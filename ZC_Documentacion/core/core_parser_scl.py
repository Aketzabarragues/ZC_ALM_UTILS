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
        if match.group(1) not in ['RegionDoc', 'Section']:
            etiquetas[match.group(1)] = limpiar_comentario(match.group(2))

    # 2. EXTRACCIÓN DE DEPENDENCIAS (<Requires>)
    dependencias_brutas = []
    if 'Requires' in etiquetas:
        for linea in etiquetas["Requires"].split('\n'):
            linea_limpia = linea.strip()
            if ':' in linea_limpia:
                partes = linea_limpia.split(':', 1)
                clave = partes[0].strip()
                
                nombres_bloques = [b.strip() for b in partes[1].split(',') if b.strip()]
                elementos = [{'nombre': b, 'url': None} for b in nombres_bloques]
                
                dependencias_brutas.append({
                    'tipo': 'normal', 
                    'clave': clave, 
                    'elementos': elementos
                })
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
            
            # Expresión regular para detectar si la línea empieza con formato de versión (ej: 01.00.00 o 1.0.0)
            patron_version = re.compile(r'^\d{1,2}\.\d{1,2}\.\d{1,2}')
            
            for linea in lineas_utiles[1:]:
                texto_limpio = linea.strip()
                
                # Si empieza por un número de versión, es una fila nueva
                if patron_version.match(texto_limpio):
                    # Separamos por 2 o más espacios, pero limitando los cortes al número de cabeceras.
                    # Así evitamos que la descripción se rompa si tiene 2 espacios seguidos dentro.
                    columnas = re.split(r'\s{2,}', texto_limpio, maxsplit=len(cabeceras) - 1)
                    columnas += [''] * (len(cabeceras) - len(columnas))
                    filas.append(columnas)
                else:
                    # Si no empieza por versión, es un salto de línea de la descripción anterior
                    if filas: # Verificamos que ya exista al menos una fila previa
                        # Concatenamos este texto a la última columna de la última fila registrada
                        filas[-1][-1] += " " + texto_limpio
                        
            changelog = {"cabeceras": cabeceras, "filas": filas}

    # 4. PARSEO DE INTERFAZ DE VARIABLES (In, Out, InOut, Temp, Constant)
    variables = []
    patron_bloques_var = r'(VAR_INPUT|VAR_OUTPUT|VAR_IN_OUT|VAR_TEMP|VAR_CONSTANT|VAR)(.*?)(?:END_VAR)'
    
    for bloque in re.finditer(patron_bloques_var, contenido, re.DOTALL):
        tipo_seccion = bloque.group(1)
        patron_linea_var = r'^\s*([a-zA-Z0-9_]+)(?:\s*\{[^}]*\})?\s*:\s*([^;]+);\s*(?://\s*(.*))?'
        
        for linea in re.finditer(patron_linea_var, bloque.group(2), re.MULTILINE):
            variables.append({
                'seccion': tipo_seccion, 
                'nombre': linea.group(1).strip(), 
                'tipo': linea.group(2).strip(), 
                'descripcion': linea.group(3).strip() if linea.group(3) else ''
            })

    # 5. PARSEO JERÁRQUICO DE SECCIONES (Anidamiento con Pila y Máquina de Estados)
    regiones = []
    pila = []
    
    rx_open = re.compile(r'///\s*<Section\s+title=["\'](.*?)["\']\s*>')
    rx_close = re.compile(r'///\s*</Section>')
    
    estado = "CODIGO" # Estados: "CODIGO", "BUSCANDO_DOC", "DESCRIPCION"
    buffer_descripcion = []
    
    for n_linea, linea in enumerate(contenido.splitlines(), start=1):
        match_open = rx_open.search(linea)
        if match_open:
            nueva_seccion = {
                'nombre': match_open.group(1).strip(),
                'nivel': len(pila) + 1,
                'doc': '',
                'codigo': [],
                'hijos': []
            }
            if pila:
                pila[-1]['hijos'].append(nueva_seccion)
            else:
                regiones.append(nueva_seccion)
            
            pila.append(nueva_seccion)
            estado = "BUSCANDO_DOC"
            continue
            
        match_close = rx_close.search(linea)
        if match_close:
            if not pila:
                log.info(f"[{nombre_bloque}] </Section> huérfano en línea {n_linea}")
            else:
                seccion_cerrada = pila.pop()
                cod_limpio = textwrap.dedent('\n'.join(seccion_cerrada['codigo'])).strip('\n\r')
                seccion_cerrada['codigo'] = textwrap.indent(cod_limpio, '    ')
            estado = "CODIGO"
            continue
            
        if not pila:
            continue # Ignoramos todo el código que no esté dentro de un <Section>
            
        if estado == "BUSCANDO_DOC":
            if linea.strip().startswith('(*'):
                estado = "DESCRIPCION"
                txt = linea.replace('(*', '', 1).strip()
                if txt: buffer_descripcion.append(txt)
                # Por si el comentario se cierra en la misma línea
                if '*)' in linea:
                    buffer_descripcion[-1] = buffer_descripcion[-1].replace('*)', '', 1).strip()
                    pila[-1]['doc'] = limpiar_comentario('\n'.join(buffer_descripcion))
                    buffer_descripcion = []
                    estado = "CODIGO"
            elif linea.strip() == '' or linea.strip().startswith('//'):
                pass # Ignoramos líneas en blanco antes de la descripción
            else:
                pila[-1]['codigo'].append(linea)
                estado = "CODIGO"
            continue
            
        if estado == "DESCRIPCION":
            if '*)' in linea:
                txt = linea.replace('*)', '', 1).strip()
                if txt: buffer_descripcion.append(txt)
                pila[-1]['doc'] = limpiar_comentario('\n'.join(buffer_descripcion))
                buffer_descripcion = []
                estado = "CODIGO"
            else:
                buffer_descripcion.append(linea)
            continue
            
        if estado == "CODIGO":
            pila[-1]['codigo'].append(linea)

    if pila:
        log.info(f"[{nombre_bloque}] Faltan {len(pila)} etiquetas </Section> por cerrar.")

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
    """
    secciones = []
    
    if bloque.get("dependencias") and len(bloque["dependencias"]) > 0:
        secciones.append({"id": "dependencias", "titulo": "Dependencias", "nivel": 1})
        
    if bloque.get("changelog"):
        secciones.append({"id": "changelog", "titulo": "Historial de Cambios", "nivel": 1})
        
    if bloque.get("variables") and len(bloque["variables"]) > 0:
        secciones.append({"id": "interfaz", "titulo": "Interfaz de Variables", "nivel": 1})
    
    if bloque.get("regiones") and len(bloque["regiones"]) > 0:
        secciones.append({"id": "logica_bloque", "titulo": "Lógica del Bloque", "nivel": 1})
        
        # Función recursiva para aplanar las <Section> y crear las anclas del menú
        def aplanar_regiones(nodos, prefijo_id=""):
            for i, nodo in enumerate(nodos):
                id_actual = f"region_{prefijo_id}{i}"
                # Reducimos un poco el texto ya que ahora cuelgan de "Lógica del Bloque"
                pref = "" if nodo['nivel'] == 1 else "↳" 
                secciones.append({
                    "id": id_actual, 
                    "titulo": f"{pref} {nodo['nombre']}", 
                    "nivel": nodo['nivel'] + 1 # Sumamos 1 para que indente en el menú lateral
                })
                if nodo['hijos']:
                    aplanar_regiones(nodo['hijos'], f"{prefijo_id}{i}_")

        aplanar_regiones(bloque.get("regiones", []))
        
    if bloque.get("contenido_original"):
        secciones.append({"id": "codigo_fuente", "titulo": "Código Fuente Completo", "nivel": 1})
        
    return secciones