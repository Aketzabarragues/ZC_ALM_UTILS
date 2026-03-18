import re
import core_logger as log

def parsear_archivo_datos(ruta_archivo):
    """
    Analiza un archivo fuente (.db o .udt) y extrae las estructuras de datos.
    Puede devolver más de un bloque si el archivo contiene TYPEs y DATA_BLOCKs.
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8', errors='replace') as f:
            contenido = f.read()

        bloques = []

        # 1. Buscar bloques UDT (TYPE ... END_TYPE)
        types = re.finditer(r'TYPE\s+"([^"]+)"(.*?)END_TYPE', contenido, re.DOTALL)
        for t in types:
            nombre = t.group(1)
            cuerpo = t.group(2)
            bloques.append(_procesar_bloque(nombre, "UDT", cuerpo))

        # 2. Buscar Bloques de Datos (DATA_BLOCK ... BEGIN)
        # Ignoramos todo lo que hay después del BEGIN porque ahí van las constantes machacadas
        dbs = re.finditer(r'DATA_BLOCK\s+"([^"]+)"(.*?)BEGIN', contenido, re.DOTALL)
        for db in dbs:
            nombre = db.group(1)
            cuerpo = db.group(2)
            bloques.append(_procesar_bloque(nombre, "DB", cuerpo))

        return bloques

    except Exception as e:
        log.error(f"Error parseando datos en {ruta_archivo}: {e}")
        return []

def _procesar_bloque(nombre, tipo_bloque, cuerpo):
    """Procesa el texto interno de un TYPE o DATA_BLOCK"""
    import re
    bloque_info = {
        "nombre_bloque": nombre,
        "tipo": tipo_bloque,
        "descripcion": "",
        "variables": []
    }

    # Extraer la descripción general (suele ser el comentario debajo de VERSION o TITLE)
    desc_match = re.search(r'VERSION.*?\n\s*//\s*(.*)', cuerpo)
    if desc_match:
        bloque_info["descripcion"] = desc_match.group(1).strip()

    lineas = cuerpo.split('\n')
    for linea in lineas:
        linea = linea.strip()
        
        # Ignoramos líneas vacías, aperturas/cierres o comentarios
        if not linea or linea.startswith('STRUCT') or linea.startswith('END_STRUCT') or linea.startswith('//'):
            continue

        # TRUCO MÁGICO: Eliminamos los atributos entre llaves de TIA Portal (ej: { S7_SetPoint := 'False'})
        linea_limpia = re.sub(r'\{[^}]*\}\s*', '', linea)

        # Regex ahora procesa la línea limpia
        var_match = re.match(r'^([a-zA-Z0-9_]+)\s*:\s*([^;]+);(?:\s*//\s*(.*))?', linea_limpia)
        if var_match:
            nombre_var = var_match.group(1).strip()
            tipo_y_valor = var_match.group(2).strip()
            comentario = var_match.group(3).strip() if var_match.group(3) else ""

            if ':=' in tipo_y_valor:
                partes = tipo_y_valor.split(':=')
                tipo_var = partes[0].strip()
                valor_defecto = partes[1].strip()
            else:
                tipo_var = tipo_y_valor
                valor_defecto = "-"

            bloque_info["variables"].append({
                "nombre": nombre_var,
                "tipo": tipo_var.replace('"', ''), 
                "valor": valor_defecto,
                "comentario": comentario
            })

    return bloque_info