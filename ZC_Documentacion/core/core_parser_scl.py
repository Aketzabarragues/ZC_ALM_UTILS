"""
Analizador (Parser) de archivos fuente SCL de TIA Portal.

Este módulo se encarga de leer el código fuente exportado (.scl), estandarizar su formato 
y extraer estructuradamente sus metadatos (etiquetas de documentación), dependencias,
interfaz de variables (Inputs, Outputs, InOuts, Temp) y lógica interna (Regiones).
"""

import os
import re
import textwrap
from core import core_logger as log


def limpiar_comentario(texto_crudo):
    """
    Estandariza los bloques de texto multilinea eliminando tabulaciones 
    y espacios invisibles introducidos por el editor nativo de TIA Portal.
    """
    if not texto_crudo: 
        return ""
    
    # 1. Transformar espacios no separables y tabs en espacios estándar
    texto = texto_crudo.replace('\xa0', ' ').replace('\t', ' ')
    
    # 2. Segmentación agnóstica del salto de línea (Windows/Unix/Mac)
    lineas = texto.splitlines()
    
    # 3. Limpieza estricta de márgenes por línea
    lineas_limpias = [linea.strip() for linea in lineas]
    
    return '\n'.join(lineas_limpias).strip()


def parsear_bloque(ruta_archivo):
    """
    Procesa un archivo .scl y estructura su contenido en un diccionario de datos.
    
    Args:
        ruta_archivo (str): Ruta absoluta al archivo fuente .scl.
        
    Returns:
        dict: Estructura de datos limpia con variables, regiones y metadatos.
    """
    log.info(f"Parseando código fuente SCL: {os.path.basename(ruta_archivo)}")
    
    with open(ruta_archivo, 'r', encoding='utf-8', errors='replace') as f:
        contenido = f.read()

    # Detección del nombre de bloque y clasificación principal (FC, FB, DB)
    match_nombre = re.search(r'(FUNCTION|FUNCTION_BLOCK|DATA_BLOCK)\s+"([^"]+)"', contenido)
    nombre_bloque = match_nombre.group(2) if match_nombre else os.path.basename(ruta_archivo).replace('.scl', '')

    # 1. EXTRACCIÓN DE ETIQUETAS XML-LIKE (<Summary>, <Remarks>, etc.)
    etiquetas = {}
    for match in re.finditer(r'///\s*<(\w+)>\s*\(\*(.*?)\*\)\s*///\s*</\1>', contenido, re.DOTALL):
        if match.group(1) != 'RegionDoc':
            etiquetas[match.group(1)] = limpiar_comentario(match.group(2))

    # 2. EXTRACCIÓN DE DEPENDENCIAS (<Requires>)
    dependencias_brutas = []
    if 'Requires' in etiquetas:
        for linea in etiquetas["Requires"].split('\n'):
            linea_limpia = linea.strip()
            if ':' in linea_limpia:
                partes = linea_limpia.split(':', 1)
                dependencias_brutas.append({'tipo': 'normal', 'clave': partes[0].strip(), 'valor': partes[1].strip(), 'url': None})
            elif linea_limpia:
                dependencias_brutas.append({'tipo': 'colspan', 'valor': linea_limpia})

    # 3. EXTRACCIÓN DEL HISTORIAL DE VERSIONES (<Changelog>)
    changelog = None
    if 'Changelog' in etiquetas:
        lineas = etiquetas["Changelog"].split('\n')
        lineas_utiles = [l for l in lineas if l.strip()]
        
        if lineas_utiles:
            cabeceras = re.split(r'\s{2,}', lineas_utiles[0].strip())
            filas = []
            for linea in lineas_utiles[1:]:
                columnas = re.split(r'\s{2,}', linea.strip())
                # Rellenado de columnas vacías por seguridad matricial (evita HTML roto)
                columnas += [''] * (len(cabeceras) - len(columnas))
                filas.append(columnas)
            changelog = {"cabeceras": cabeceras, "filas": filas}

    # 4. PARSEO DE INTERFAZ DE VARIABLES (In, Out, InOut, Temp, Constant)
    variables = []
    # Patrón delimitador de las áreas de variables
    patron_bloques_var = r'(VAR_INPUT|VAR_OUTPUT|VAR_IN_OUT|VAR_TEMP|VAR_CONSTANT|VAR)(.*?)(?:END_VAR)'
    
    for bloque in re.finditer(patron_bloques_var, contenido, re.DOTALL):
        tipo_seccion = bloque.group(1)
        
        # Patrón de línea modificado:
        # Se incluye un grupo no capturable (?:\s*\{[^}]*\})? para absorber metadatos
        # inyectados por TIA Portal como {InstructionName := 'DTL'; LibVersion := '1.0'}
        patron_linea_var = r'^\s*([a-zA-Z0-9_]+)(?:\s*\{[^}]*\})?\s*:\s*([^;]+);\s*(?://\s*(.*))?'
        
        for linea in re.finditer(patron_linea_var, bloque.group(2), re.MULTILINE):
            variables.append({
                'seccion': tipo_seccion, 
                'nombre': linea.group(1).strip(), 
                'tipo': linea.group(2).strip(), 
                'descripcion': linea.group(3).strip() if linea.group(3) else ''
            })

    # 5. PARSEO JERÁRQUICO DE REGIONES Y CÓDIGO INTERNO
    regiones, pila, doc_pendiente = [], [], "Sin documentación específica."
    patron_tokens = r'(?P<doc>///\s*<RegionDoc>\s*\(\*(?P<texto_doc>.*?)\*\)\s*///\s*</RegionDoc>)|(?P<region>^[ \t]*REGION\s+(?P<nombre_region>[^\n\r]+))|(?P<endregion>^[ \t]*END_REGION)'
    
    for match in re.finditer(patron_tokens, contenido, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE):
        if match.group('doc'):
            doc_pendiente = limpiar_comentario(match.group('texto_doc'))
            
        elif match.group('region'):
            nueva_region = {
                'doc': doc_pendiente, 
                'nombre': match.group('nombre_region').strip(), 
                'nivel': len(pila) + 1, 
                'start_idx': match.end(), 
                'hijos': [], 
                'codigo': ''
            }
            pila.append(nueva_region)
            regiones.append(nueva_region)
            doc_pendiente = "Sin documentación específica."
            
        elif match.group('endregion') and pila:
            region_cerrada = pila.pop()
            
            # Extracción y limpieza indentada del bloque de código nativo
            codigo_bruto = contenido[region_cerrada['start_idx']:match.start()]
            codigo_limpio = textwrap.dedent(codigo_bruto).strip('\n\r')
            region_cerrada['codigo'] = textwrap.indent(codigo_limpio, '    ')
            
            if pila: 
                pila[-1]['hijos'].append(region_cerrada['nombre'])

    # Ensamblaje del objeto final (DTO - Data Transfer Object)
    bloque_data = {
        "nombre_bloque": nombre_bloque,
        "etiquetas": etiquetas,
        "dependencias": dependencias_brutas,
        "changelog": changelog,
        "variables": variables,
        "regiones": regiones,
        "contenido_original": contenido
    }

    return bloque_data


def generar_secciones_menu(bloque):
    """
    Construye la lista de índices (anclas) para el menú lateral web.
    
    Evalúa de forma dinámica la existencia de dependencias, variables o historial
    para generar un índice limpio y coherente con el contenido real del bloque.
    """
    secciones = []
    
    if bloque.get("dependencias") and len(bloque["dependencias"]) > 0:
        secciones.append({"id": "dependencias", "titulo": "Dependencias", "nivel": 1})
        
    if bloque.get("changelog"):
        secciones.append({"id": "changelog", "titulo": "Historial de Cambios", "nivel": 1})
        
    if bloque.get("variables") and len(bloque["variables"]) > 0:
        secciones.append({"id": "interfaz", "titulo": "Interfaz de Variables", "nivel": 1})
        
    # Árbol dinámico de lógicas de proceso
    for i, r in enumerate(bloque.get("regiones", [])):
        prefijo = "Lógica:" if r['nivel'] == 1 else "↳ Sub-lógica:"
        secciones.append({
            "id": f"region_{i}", 
            "titulo": f"{prefijo} {r['nombre']}", 
            "nivel": r['nivel']
        })
        
    if bloque.get("contenido_original"):
        secciones.append({"id": "codigo_fuente", "titulo": "Código Fuente Completo", "nivel": 1})
        
    return secciones