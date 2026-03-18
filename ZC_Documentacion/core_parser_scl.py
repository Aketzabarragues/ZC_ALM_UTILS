import os
import re
import textwrap
import core_logger as log

def limpiar_comentario(texto_crudo):
    """
    Aniquilación total de caracteres invisibles, tabs y espacios irrompibles.
    """
    if not texto_crudo: 
        return ""
    
    # 1. Transformar espacios raros y tabs en espacios normales
    texto = texto_crudo.replace('\xa0', ' ').replace('\t', ' ')
    
    # 2. Partimos el texto independientemente del salto de línea que use Windows/TIA Portal
    lineas = texto.splitlines()
    
    # 3. .strip() se come sin piedad todo el espacio por la izquierda y la derecha
    lineas_limpias = [linea.strip() for linea in lineas]
    
    return '\n'.join(lineas_limpias).strip()




def parsear_bloque(ruta_archivo):
    """Lee un archivo .scl y devuelve un diccionario puro (sin HTML) con toda su info."""
    log.info(f"Parseando bloque SCL: {os.path.basename(ruta_archivo)}")
    
    with open(ruta_archivo, 'r', encoding='utf-8', errors='replace') as f:
        contenido = f.read()

    match_nombre = re.search(r'(FUNCTION|FUNCTION_BLOCK|DATA_BLOCK)\s+"([^"]+)"', contenido)
    nombre_bloque = match_nombre.group(2) if match_nombre else os.path.basename(ruta_archivo).replace('.scl', '')

    # 1. ETIQUETAS (Summary, Remarks, etc.)
    etiquetas = {}
    for match in re.finditer(r'///\s*<(\w+)>\s*\(\*(.*?)\*\)\s*///\s*</\1>', contenido, re.DOTALL):
        if match.group(1) != 'RegionDoc':
            # PASAMOS EL TEXTO POR LA FUNCIÓN BLINDADA
            etiquetas[match.group(1)] = limpiar_comentario(match.group(2))

    # 2. DEPENDENCIAS
    dependencias_brutas = []
    if 'Requires' in etiquetas:
        for linea in etiquetas["Requires"].split('\n'):
            linea_limpia = linea.strip()
            if ':' in linea_limpia:
                partes = linea_limpia.split(':', 1)
                dependencias_brutas.append({'tipo': 'normal', 'clave': partes[0].strip(), 'valor': partes[1].strip(), 'url': None})
            elif linea_limpia:
                dependencias_brutas.append({'tipo': 'colspan', 'valor': linea_limpia})

    # 3. CHANGELOG
    changelog = None
    if 'Changelog' in etiquetas:
        lineas = etiquetas["Changelog"].split('\n')
        lineas_utiles = [l for l in lineas if l.strip()]
        if lineas_utiles:
            cabeceras = re.split(r'\s{2,}', lineas_utiles[0].strip())
            filas = []
            for linea in lineas_utiles[1:]:
                columnas = re.split(r'\s{2,}', linea.strip())
                columnas += [''] * (len(cabeceras) - len(columnas))
                filas.append(columnas)
            changelog = {"cabeceras": cabeceras, "filas": filas}

    # 4. VARIABLES
    variables = []
    for bloque in re.finditer(r'(VAR_INPUT|VAR_OUTPUT|VAR_IN_OUT|VAR_TEMP|VAR)(.*?)(?:END_VAR)', contenido, re.DOTALL):
        tipo_seccion = bloque.group(1)
        for linea in re.finditer(r'^\s*([a-zA-Z0-9_]+)\s*:\s*([^;]+);\s*(?://\s*(.*))?', bloque.group(2), re.MULTILINE):
            variables.append({'seccion': tipo_seccion, 'nombre': linea.group(1), 'tipo': linea.group(2), 'descripcion': linea.group(3).strip() if linea.group(3) else ''})

    # 5. REGIONES
    regiones, pila, doc_pendiente = [], [], "Sin documentación específica."
    patron_tokens = r'(?P<doc>///\s*<RegionDoc>\s*\(\*(?P<texto_doc>.*?)\*\)\s*///\s*</RegionDoc>)|(?P<region>^[ \t]*REGION\s+(?P<nombre_region>[^\n\r]+))|(?P<endregion>^[ \t]*END_REGION)'
    
    for match in re.finditer(patron_tokens, contenido, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE):
        if match.group('doc'):
            # PASAMOS EL TEXTO DE LA REGIÓN POR LA FUNCIÓN BLINDADA
            doc_pendiente = limpiar_comentario(match.group('texto_doc'))
        elif match.group('region'):
            nueva_region = {'doc': doc_pendiente, 'nombre': match.group('nombre_region').strip(), 'nivel': len(pila) + 1, 'start_idx': match.end(), 'hijos': [], 'codigo': ''}
            pila.append(nueva_region)
            regiones.append(nueva_region)
            doc_pendiente = "Sin documentación específica."
        elif match.group('endregion') and pila:
            region_cerrada = pila.pop()
            
            # Extraer y formatear el código SCL interno
            codigo_bruto = contenido[region_cerrada['start_idx']:match.start()]
            codigo_limpio = textwrap.dedent(codigo_bruto).strip()
            region_cerrada['codigo'] = textwrap.indent(codigo_limpio, '    ')
            
            if pila: pila[-1]['hijos'].append(region_cerrada['nombre'])

    # OBJETO FINAL
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
    """Genera las entradas del menú lateral basadas en el contenido real del bloque."""
    secciones = []
    
    # 1. Secciones fijas (Nivel 1 dentro del bloque)
    # (Omitimos 'Descripción General' porque al pulsar en el nombre del bloque ya va arriba del todo)
    
    if bloque.get("dependencias") and len(bloque["dependencias"]) > 0:
        secciones.append({"id": "dependencias", "titulo": "Dependencias", "nivel": 1})
        
    if bloque.get("changelog"):
        secciones.append({"id": "changelog", "titulo": "Historial de Cambios", "nivel": 1})
        
    if bloque.get("variables") and len(bloque["variables"]) > 0:
        secciones.append({"id": "interfaz", "titulo": "Interfaz de Variables", "nivel": 1})
        
    # 2. Regiones de código (Respetando su anidamiento/nivel interno)
    for i, r in enumerate(bloque.get("regiones", [])):
        # Añadimos un pequeño prefijo para que quede claro en el menú qué es cada cosa
        prefijo = "Lógica:" if r['nivel'] == 1 else "↳ Sub-lógica:"
        secciones.append({
            "id": f"region_{i}", 
            "titulo": f"{prefijo} {r['nombre']}", 
            "nivel": r['nivel']
        })
        
    # 3. Código Fuente (Nivel 1)
    if bloque.get("contenido_original"):
        secciones.append({"id": "codigo_fuente", "titulo": "Código Fuente Completo", "nivel": 1})
        
    return secciones