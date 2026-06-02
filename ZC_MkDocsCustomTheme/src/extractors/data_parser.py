# src/extractors/data_parser.py
import re
from pathlib import Path
from typing import List
from domain.models import BlockType, SiemensBlock, VariableDef, SystemInfo

def parsear_archivo_datos(ruta_archivo: Path) -> List[SiemensBlock]:
    try:
        contenido = ruta_archivo.read_text(encoding='utf-8', errors='replace')
        bloques = []

        # 1. Extracción de UDTs
        for match in re.finditer(r'TYPE\s+"([^"]+)"(.*?)END_TYPE', contenido, flags=re.DOTALL):
            bloques.append(_procesar_bloque(match.group(1), BlockType.UDT, match.group(2), contenido))

        # 2. Extracción de DBs
        for match in re.finditer(r'DATA_BLOCK\s+"([^"]+)"(.*?)BEGIN', contenido, flags=re.DOTALL):
            bloques.append(_procesar_bloque(match.group(1), BlockType.DB, match.group(2), contenido))

        return bloques
    except Exception as e:
        print(f"[ERROR] Fallo en {ruta_archivo}: {e}")
        return []

def _procesar_bloque(nombre: str, tipo_bloque: BlockType, cuerpo: str, contenido_completo: str) -> SiemensBlock:
    descripcion = None
    match_desc = re.search(r'VERSION.*?\n\s*//\s*(.*)', cuerpo)
    if match_desc:
        descripcion = match_desc.group(1).strip()

    variables = []
    for linea in cuerpo.splitlines():
        linea_limpia = linea.strip()
        if not linea_limpia or linea_limpia.startswith(('STRUCT', 'END_STRUCT', '//')):
            continue

        linea_sin_metadatos = re.sub(r'\{[^}]*\}\s*', '', linea_limpia)
        match_var = re.match(r'^([a-zA-Z0-9_]+)\s*:\s*([^;]+);(?:\s*//\s*(.*))?', linea_sin_metadatos)
        
        if match_var:
            t_y_v = match_var.group(2).strip()
            variables.append(VariableDef(
                name=match_var.group(1).strip(),
                data_type=t_y_v.split(':=')[0].strip().replace('"', ''),
                default_value=t_y_v.split(':=')[1].strip() if ':=' in t_y_v else "-",
                comment=match_var.group(3).strip() if match_var.group(3) else None,
                is_retain='RETAIN' in linea_limpia.upper()
            ))

    # Creamos el modelo cumpliendo los nuevos requisitos del Custom Theme
    return SiemensBlock(
        name=nombre,
        block_type=tipo_bloque,
        description=descripcion,
        system_info=SystemInfo(), # Valores por defecto
        sections={"Variables": variables} if variables else {},
        source_code=contenido_completo
    )