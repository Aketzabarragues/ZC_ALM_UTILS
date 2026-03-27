"""
Analizador (Parser) de archivos fuente SCL de TIA Portal - ESTÁNDAR SIEMENS LGF.
"""

import os
import re
import textwrap
from core import core_logger as log
import markdown

def limpiar_texto(texto):
    if not texto: return ""
    return texto.replace('\xa0', ' ').replace('\t', ' ').strip()

def parsear_bloque(ruta_archivo):
    log.info(f"Parseando código fuente SCL (Formato Siemens): {os.path.basename(ruta_archivo)}")
    
    with open(ruta_archivo, 'r', encoding='utf-8', errors='replace') as f:
        contenido = f.read()

    match_nombre = re.search(r'(FUNCTION|FUNCTION_BLOCK|DATA_BLOCK)\s+"([^"]+)"', contenido)
    nombre_bloque = match_nombre.group(2) if match_nombre else os.path.basename(ruta_archivo).replace('.scl', '')

    etiquetas = {}
    dependencias_brutas = []
    changelog = None

    # EXTRACCIÓN DE PROPIEDADES NATIVAS DEL BLOQUE
    match_version = re.search(r'^VERSION\s*:\s*(.*)', contenido, re.MULTILINE | re.IGNORECASE)
    if match_version: etiquetas['Version_Bloque'] = match_version.group(1).strip()
        
    match_author = re.search(r'^AUTHOR\s*:\s*(.*)', contenido, re.MULTILINE | re.IGNORECASE)
    if match_author: etiquetas['Author_Bloque'] = match_author.group(1).strip()
        
    match_family = re.search(r'^FAMILY\s*:\s*(.*)', contenido, re.MULTILINE | re.IGNORECASE)
    if match_family: etiquetas['Family_Bloque'] = match_family.group(1).strip()

    # 1. EXTRACCIÓN DE LA CABECERA (REGION Description header)
    match_header = re.search(r'REGION\s+(?:Description header|DESCRIPCION)\s*(.*?)\s*END_REGION\s+(?:Description header|DESCRIPCION)', contenido, re.DOTALL | re.IGNORECASE)
    if match_header:
        header_text = match_header.group(1)
        
        campos_simples = ['Title', 'Library/Family', 'Author', 'Tested on System', 'Engineering', 'Restrictions']
        for campo in campos_simples:
            match_campo = re.search(rf'//\s*{campo}:\s*(.*)', header_text)
            if match_campo:
                etiquetas[campo] = limpiar_texto(match_campo.group(1))

        # --- LÓGICA PARA COMMENT/FUNCTION CON MARKDOWN ---
        # --- LÓGICA PARA COMMENT/FUNCTION CON MARKDOWN ---
        import markdown 

        match_comment = re.search(r'//\s*Comment/Function:\s*(.*?)(?=\n\s*//\s*[A-Za-z/ ]+:|\n\s*//---)', header_text, re.DOTALL)
        if match_comment:
            raw_comment = match_comment.group(1)
            
            match_block = re.search(r'\(\*(.*?)\*\)', raw_comment, re.DOTALL)
            if match_block:
                texto_crudo = match_block.group(1)
                
                # 1. Convertimos tabulaciones literales a 2 espacios
                texto_crudo = texto_crudo.replace('\t', '  ')
                texto_limpio = textwrap.dedent(texto_crudo).strip()
            else:
                lineas_limpias = [l.replace('//', '', 1).strip() for l in raw_comment.splitlines()]
                texto_limpio = '\n'.join([l for l in lineas_limpias if l]).strip()
            
            # 2. EL TRUCO ANTIMAQUINA DE ESCRIBIR: 
            # Reemplazamos todos los grupos de 4 espacios por 2 espacios. 
            # Esto evita el comportamiento de "Bloque de código" pero mantiene la anidación de las listas.
            texto_limpio = texto_limpio.replace('    ', '  ')
            
            # 3. Forzar doble salto de línea antes de viñetas (Mejorado para detectar saltos de línea de Windows \r\n)
            texto_limpio = re.sub(r'([^\n\r])\r?\n(\s*[-*]\s)', r'\1\n\n\2', texto_limpio)
            
            # 4. Generar HTML limpio
            etiquetas['Comment/Function'] = markdown.markdown(texto_limpio, extensions=['extra', 'nl2br'])
        # -------------------------------------------------------------
        # -------------------------------------------------------------

        match_req = re.search(r'//\s*Requirements:\s*(.*?)(?=\n\s*//---)', header_text, re.DOTALL)
        if match_req:
            for rline in match_req.group(1).splitlines():
                rline_clean = rline.replace('//', '', 1).strip()
                if rline_clean.startswith('-'):
                    partes = rline_clean[1:].split(':', 1)
                    if len(partes) == 2:
                        clave = partes[0].strip()
                        nombres = [n.strip() for n in partes[1].split(',') if n.strip()]
                        elementos = [{'nombre': n, 'url': None} for n in nombres]
                        dependencias_brutas.append({'tipo': 'normal', 'clave': clave, 'elementos': elementos})

        match_change = re.search(r'//\s*Change log table:\s*\n(.*?)(?=\n\s*//===)', header_text, re.DOTALL)
        if match_change:
            cl_lines = match_change.group(1).splitlines()
            utiles = [l.replace('//', '', 1).strip() for l in cl_lines if l.strip() and not l.strip().startswith('//---')]
            if len(utiles) > 1:
                cabeceras = [c.strip() for c in utiles[0].split('|')]
                filas = [[c.strip() for c in fila_str.split('|')] for fila_str in utiles[1:]]
                changelog = {"cabeceras": cabeceras, "filas": filas}

    # 2. PARSEO DE INTERFAZ DE VARIABLES AGRUPADAS
    variables_agrupadas = {}
    
    patron_bloques_var = r'(VAR_INPUT\s+RETAIN|VAR_INPUT|VAR_OUTPUT\s+RETAIN|VAR_OUTPUT|VAR_IN_OUT\s+RETAIN|VAR_IN_OUT|VAR_TEMP|VAR_CONSTANT|VAR\s+CONSTANT|VAR\s+RETAIN|VAR)(.*?)(?:END_VAR)'
    
    mapeo_secciones = {
        'VAR_INPUT': 'Entradas',
        'VAR_INPUT RETAIN': 'Entradas',
        'VAR_OUTPUT': 'Salidas',
        'VAR_OUTPUT RETAIN': 'Salidas',
        'VAR_IN_OUT': 'Entrada/Salida',
        'VAR_IN_OUT RETAIN': 'Entrada/Salida',
        'VAR_TEMP': 'Temporales',
        'VAR_CONSTANT': 'Constantes',
        'VAR CONSTANT': 'Constantes',
        'VAR': 'Estáticas',
        'VAR RETAIN': 'Estáticas'
    }

    for bloque in re.finditer(patron_bloques_var, contenido, re.DOTALL | re.IGNORECASE):
        tipo_raw = re.sub(r'\s+', ' ', bloque.group(1).strip().upper())
        nombre_seccion = mapeo_secciones.get(tipo_raw, tipo_raw)
        
        # Averiguamos si la sección en la que estamos declara variables remanentes
        es_remanente = 'RETAIN' in tipo_raw
        
        if nombre_seccion not in variables_agrupadas:
            variables_agrupadas[nombre_seccion] = []
            
        patron_linea_var = r'^\s*([a-zA-Z0-9_]+)(?:\s*\{[^}]*\})?\s*:\s*([^;]+);\s*(?://\s*(.*))?'
        
        for linea in re.finditer(patron_linea_var, bloque.group(2), re.MULTILINE):
            variables_agrupadas[nombre_seccion].append({
                'nombre': linea.group(1).strip(), 
                'tipo': linea.group(2).strip(), 
                'descripcion': linea.group(3).strip() if linea.group(3) else '',
                'is_retain': es_remanente # Guardamos el flag booleano
            })

    variables_agrupadas = {k: v for k, v in variables_agrupadas.items() if v}

    return {
        "nombre_bloque": nombre_bloque,
        "etiquetas": etiquetas,
        "dependencias": dependencias_brutas,
        "changelog": changelog,
        "variables_agrupadas": variables_agrupadas,
        "contenido_original": contenido
    }

def generar_secciones_menu(bloque):
    secciones = []
    if bloque.get("etiquetas") and "Comment/Function" in bloque["etiquetas"]:
        secciones.append({"id": "descripcion", "titulo": "Descripción Funcional", "nivel": 1})
    if bloque.get("changelog"):
        secciones.append({"id": "changelog", "titulo": "Historial de Cambios", "nivel": 1})
    if bloque.get("variables_agrupadas"):
        secciones.append({"id": "interfaz", "titulo": "Interfaz del Bloque", "nivel": 1})
    if bloque.get("dependencias"):
        secciones.append({"id": "dependencias", "titulo": "Dependencias", "nivel": 1})
    if bloque.get("contenido_original"):
        secciones.append({"id": "codigo_fuente", "titulo": "Código Fuente", "nivel": 1})
    return secciones