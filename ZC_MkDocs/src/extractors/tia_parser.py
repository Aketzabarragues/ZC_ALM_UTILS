import re
from pathlib import Path
from typing import List
from domain.models import BlockType, SiemensBlock, VariableDef

def parsear_archivo_datos(ruta_archivo: Path) -> List[SiemensBlock]:
    """
    Analiza un archivo físico (.db o .udt) para extraer sus bloques lógicos
    y los devuelve como modelos Pydantic validados.
    """
    try:
        contenido = ruta_archivo.read_text(encoding='utf-8', errors='replace')
        bloques: List[SiemensBlock] = []

        # 1. Extracción de Tipos de Datos de Usuario (UDT)
        patron_udt = r'TYPE\s+"([^"]+)"(.*?)END_TYPE'
        for match in re.finditer(patron_udt, contenido, flags=re.DOTALL):
            bloques.append(_procesar_bloque(match.group(1), BlockType.UDT, match.group(2)))

        # 2. Extracción de Bloques de Datos (DB)
        patron_db = r'DATA_BLOCK\s+"([^"]+)"(.*?)BEGIN'
        for match in re.finditer(patron_db, contenido, flags=re.DOTALL):
            bloques.append(_procesar_bloque(match.group(1), BlockType.DB, match.group(2)))

        return bloques
    except Exception as e:
        # Aquí usarías un logger real en producción
        print(f"[ERROR] Fallo en {ruta_archivo}: {e}")
        return []

def _procesar_bloque(nombre: str, tipo_bloque: BlockType, cuerpo: str) -> SiemensBlock:
    """Procesa el contenido y construye el modelo Pydantic."""
    
    descripcion = None
    match_desc = re.search(r'VERSION.*?\n\s*//\s*(.*)', cuerpo)
    if match_desc:
        descripcion = match_desc.group(1).strip()

    variables: List[VariableDef] = []
    lineas = cuerpo.splitlines()
    
    for linea in lineas:
        linea_limpia = linea.strip()
        if not linea_limpia or linea_limpia.startswith(('STRUCT', 'END_STRUCT', '//')):
            continue

        linea_sin_metadatos = re.sub(r'\{[^}]*\}\s*', '', linea_limpia)
        patron_variable = r'^([a-zA-Z0-9_]+)\s*:\s*([^;]+);(?:\s*//\s*(.*))?'
        match_var = re.match(patron_variable, linea_sin_metadatos)
        
        if match_var:
            nombre_var = match_var.group(1).strip()
            tipo_y_valor = match_var.group(2).strip()
            comentario = match_var.group(3).strip() if match_var.group(3) else None

            if ':=' in tipo_y_valor:
                partes = tipo_y_valor.split(':=')
                tipo_var = partes[0].strip()
                valor_defecto = partes[1].strip()
            else:
                tipo_var = tipo_y_valor
                valor_defecto = "-"

            variables.append(VariableDef(
                name=nombre_var,
                data_type=tipo_var.replace('"', ''),
                default_value=valor_defecto,
                comment=comentario
            ))

    return SiemensBlock(
        name=nombre,
        block_type=tipo_bloque,
        description=descripcion,
        variables=variables
    )