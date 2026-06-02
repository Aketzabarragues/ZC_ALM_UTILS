import re
import textwrap
from pathlib import Path
from domain.models import BlockType, SiemensBlock, VariableDef, SystemInfo, DependencyDef

def parsear_scl(ruta_archivo: Path) -> SiemensBlock:
    contenido = ruta_archivo.read_text(encoding='utf-8', errors='replace')

    match_nombre = re.search(r'(FUNCTION|FUNCTION_BLOCK)\s+"([^"]+)"', contenido, re.IGNORECASE)
    if not match_nombre:
        raise ValueError(f"No se encontró definición de bloque en {ruta_archivo.name}")
        
    tipo_bloque = BlockType.FB if "BLOCK" in match_nombre.group(1).upper() else BlockType.FC
    nombre_bloque = match_nombre.group(2)

    version = (re.search(r'^VERSION\s*:\s*(.*)', contenido, re.M | re.I) or [None, None])[1]
    author = (re.search(r'^AUTHOR\s*:\s*(.*)', contenido, re.M | re.I) or [None, None])[1]
    family = (re.search(r'^FAMILY\s*:\s*(.*)', contenido, re.M | re.I) or [None, None])[1]

    sys_info = SystemInfo()
    description = restrictions = changelog_md = None
    dependencies = []

    # Extraer todo el bloque de documentación corporativa
    match_region = re.search(r'REGION\s+DESCRIPCION\s*\(\*(.*?)\*\)\s*END_REGION', contenido, re.DOTALL | re.IGNORECASE)
    if match_region:
        header_text = match_region.group(1)
        
        # 1. Información del Sistema
        sys_match = re.search(r'###\s*Información del Sistema\s*(.*?)(?=\n\s*---|###|\*\))', header_text, re.DOTALL | re.IGNORECASE)
        if sys_match:
            lineas_tabla = [l.strip() for l in sys_match.group(1).splitlines() if l.strip().startswith('|')]
            if len(lineas_tabla) >= 3:
                valores = [v.strip() for v in lineas_tabla[2].split('|') if v.strip()]
                if len(valores) >= 2:
                    sys_info.hardware = valores[0]
                    sys_info.engineering = valores[1]

        # 2. Descripción Funcional y Restricciones
        desc_match = re.search(r'###\s*Descripción Funcional\s*(.*?)(?=\n\s*---|###|\*\))', header_text, re.DOTALL | re.IGNORECASE)
        if desc_match:
            raw_desc = desc_match.group(1).strip()
            rest_match = re.search(r'>\s*\*\*Restricciones:\*\*(.*)', raw_desc, re.IGNORECASE)
            if rest_match:
                restrictions = rest_match.group(1).strip()
                raw_desc = re.sub(r'>\s*\*\*Restricciones:\*\*.*', '', raw_desc, flags=re.IGNORECASE).strip()
            description = textwrap.dedent(raw_desc).strip()

        # 3. Dependencias Requeridas
        req_match = re.search(r'###\s*Dependencias Requeridas\s*(.*?)(?=\n\s*---|###|\*\))', header_text, re.DOTALL | re.IGNORECASE)
        if req_match:
            lineas_tabla = [l.strip() for l in req_match.group(1).splitlines() if l.strip().startswith('|')]
            for linea in lineas_tabla[2:]: # Saltar cabeceras
                valores = [v.strip() for v in linea.split('|') if v.strip()]
                if len(valores) >= 2 and valores[1] != '-':
                    dependencies.append(DependencyDef(type=valores[0], elements=valores[1]))

        # 4. Historial de Cambios
        cl_match = re.search(r'###\s*Historial de Cambios\s*(.*?)(?=\n\s*---|###|\*\))', header_text, re.DOTALL | re.IGNORECASE)
        if cl_match:
            changelog_md = cl_match.group(1).strip()

    # Variables
    sections = {}
    patron_bloques_var = r'(VAR_INPUT\s+RETAIN|VAR_INPUT|VAR_OUTPUT\s+RETAIN|VAR_OUTPUT|VAR_IN_OUT\s+RETAIN|VAR_IN_OUT|VAR_TEMP|VAR_CONSTANT|VAR\s+CONSTANT|VAR\s+RETAIN|VAR)(.*?)(?:END_VAR)'
    mapeo_secciones = {
        'VAR_INPUT': 'Entradas', 'VAR_INPUT RETAIN': 'Entradas', 'VAR_OUTPUT': 'Salidas', 'VAR_OUTPUT RETAIN': 'Salidas',
        'VAR_IN_OUT': 'Entrada/Salida', 'VAR_IN_OUT RETAIN': 'Entrada/Salida', 'VAR_TEMP': 'Temporales', 
        'VAR_CONSTANT': 'Constantes', 'VAR CONSTANT': 'Constantes', 'VAR': 'Estáticas', 'VAR RETAIN': 'Estáticas'
    }

    for bloque in re.finditer(patron_bloques_var, contenido, re.DOTALL | re.IGNORECASE):
        tipo_raw = re.sub(r'\s+', ' ', bloque.group(1).strip().upper())
        nombre_seccion = mapeo_secciones.get(tipo_raw, tipo_raw)
        if nombre_seccion not in sections: sections[nombre_seccion] = []
            
        for linea in re.finditer(r'^\s*([a-zA-Z0-9_]+)(?:\s*\{[^}]*\})?\s*:\s*([^;]+);\s*(?://\s*(.*))?', bloque.group(2), re.MULTILINE):
            t_y_v = linea.group(2).strip()
            sections[nombre_seccion].append(VariableDef(
                name=linea.group(1).strip(),
                data_type=t_y_v.split(':=')[0].strip().replace('"', ''),
                default_value=t_y_v.split(':=')[1].strip() if ':=' in t_y_v else "-",
                comment=linea.group(3).strip() if linea.group(3) else None,
                is_retain='RETAIN' in tipo_raw
            ))

    return SiemensBlock(
        name=nombre_bloque, block_type=tipo_bloque, description=description,
        author=author, version=version, family=family, system_info=sys_info,
        restrictions=restrictions, changelog_md=changelog_md,
        dependencies=dependencies, sections=sections, source_code=contenido
    )