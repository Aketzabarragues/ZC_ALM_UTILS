"""
Analizador (Parser) de Estructuras de Datos de TIA Portal.

Este módulo procesa archivos fuente exportados que contienen la definición de
Bloques de Datos (DB) y Tipos de Datos de Usuario (UDT). Extrae metadatos,
descripciones globales y la estructura interna de variables, incluyendo sus 
tipos, valores por defecto y comentarios asociados.
"""

import re
import core_logger as log


def parsear_archivo_datos(ruta_archivo):
    """
    Analiza un archivo físico (.db o .udt) para extraer sus bloques lógicos.
    
    Un único archivo fuente de Siemens puede contener múltiples declaraciones 
    (por ejemplo, varios TYPEs). Esta función fragmenta el archivo en bloques
    y delega el análisis sintáctico de cada uno.

    Args:
        ruta_archivo (str): Ruta absoluta al archivo fuente a procesar.

    Returns:
        list: Lista de diccionarios (Data Transfer Objects) con la información 
              estructurada de cada bloque de datos encontrado.
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8', errors='replace') as f:
            contenido = f.read()

        bloques = []

        # 1. Extracción de Tipos de Datos de Usuario (UDT)
        # El patrón busca bloques delimitados por las palabras clave TYPE y END_TYPE
        patron_udt = r'TYPE\s+"([^"]+)"(.*?)END_TYPE'
        for match in re.finditer(patron_udt, contenido, flags=re.DOTALL):
            nombre_udt = match.group(1)
            cuerpo_udt = match.group(2)
            bloques.append(_procesar_bloque(nombre_udt, "UDT", cuerpo_udt))

        # 2. Extracción de Bloques de Datos Globales o de Instancia (DB)
        # Se procesa únicamente la cabecera declarativa hasta la cláusula BEGIN.
        # Se ignora el código posterior ya que contiene sobreescrituras estáticas de valores.
        patron_db = r'DATA_BLOCK\s+"([^"]+)"(.*?)BEGIN'
        for match in re.finditer(patron_db, contenido, flags=re.DOTALL):
            nombre_db = match.group(1)
            cuerpo_db = match.group(2)
            bloques.append(_procesar_bloque(nombre_db, "DB", cuerpo_db))

        return bloques

    except Exception as e:
        log.error(f"Fallo estructural durante el parseo de datos en {ruta_archivo}: {str(e)}")
        return []


def _procesar_bloque(nombre, tipo_bloque, cuerpo):
    """
    Procesa el contenido interno de un bloque de datos (TYPE o DATA_BLOCK).

    Aplica limpieza de metadatos del compilador y extrae línea por línea
    las variables declaradas, identificando su identificador, tipo de dato, 
    valor de inicialización y comentario asociado.

    Args:
        nombre (str): Identificador del bloque (ej. "DB_PROCESO").
        tipo_bloque (str): Clasificación funcional ("DB" o "UDT").
        cuerpo (str): Cadena de texto con la definición interna del bloque.

    Returns:
        dict: Objeto estandarizado con los metadatos y la colección de variables.
    """
    bloque_info = {
        "nombre_bloque": nombre,
        "tipo": tipo_bloque,
        "descripcion": "",
        "variables": []
    }

    # Extracción de la descripción global del bloque
    # Típicamente ubicada como comentario inmediatamente después de la declaración de VERSION
    match_desc = re.search(r'VERSION.*?\n\s*//\s*(.*)', cuerpo)
    if match_desc:
        bloque_info["descripcion"] = match_desc.group(1).strip()

    # Análisis secuencial de la estructura de variables
    lineas = cuerpo.splitlines()
    
    for linea in lineas:
        linea_limpia = linea.strip()
        
        # Filtro: Omisión de líneas vacías, delimitadores de jerarquía anidada (STRUCT) 
        # y líneas exclusivas de comentarios.
        if not linea_limpia or linea_limpia.startswith('STRUCT') or linea_limpia.startswith('END_STRUCT') or linea_limpia.startswith('//'):
            continue

        # Neutralización de metadatos de configuración inyectados por el IDE de TIA Portal
        # Ej: { S7_SetPoint := 'False'; ExternalVisible := 'False' }
        linea_sin_metadatos = re.sub(r'\{[^}]*\}\s*', '', linea_limpia)

        # Extracción léxica de los componentes de la variable
        # Grupos esperados: (1) Nombre, (2) Tipo y posible Valor, (3) Comentario opcional
        patron_variable = r'^([a-zA-Z0-9_]+)\s*:\s*([^;]+);(?:\s*//\s*(.*))?'
        match_var = re.match(patron_variable, linea_sin_metadatos)
        
        if match_var:
            nombre_var = match_var.group(1).strip()
            tipo_y_valor = match_var.group(2).strip()
            comentario = match_var.group(3).strip() if match_var.group(3) else ""

            # Desacoplamiento del tipo de dato y su valor de inicialización (si existe)
            if ':=' in tipo_y_valor:
                partes = tipo_y_valor.split(':=')
                tipo_var = partes[0].strip()
                valor_defecto = partes[1].strip()
            else:
                tipo_var = tipo_y_valor
                valor_defecto = "-"

            bloque_info["variables"].append({
                "nombre": nombre_var,
                # Limpieza de comillas residuales en tipos envolventes (ej. "UDT_Motor")
                "tipo": tipo_var.replace('"', ''), 
                "valor": valor_defecto,
                "comentario": comentario
            })

    return bloque_info