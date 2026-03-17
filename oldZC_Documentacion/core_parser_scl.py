import os
import re

def parsear_scl(ruta_archivo):
    """Lee el SCL y devuelve todos los datos limpios y estructurados."""
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()

    match_nombre = re.search(r'(FUNCTION|FUNCTION_BLOCK|DATA_BLOCK)\s+"([^"]+)"', contenido)
    nombre_bloque = match_nombre.group(2) if match_nombre else os.path.basename(ruta_archivo).replace('.scl', '')

    etiquetas = {}
    for match in re.finditer(r'///\s*<(\w+)>\s*\(\*(.*?)\*\)\s*///\s*</\1>', contenido, re.DOTALL):
        if match.group(1) != 'RegionDoc':
            etiquetas[match.group(1)] = match.group(2).strip()

    # Estructuramos Dependencias para Jinja2
    dependencias = []
    if 'Requires' in etiquetas:
        for linea in etiquetas["Requires"].strip().split('\n'):
            if ':' in linea:
                partes = linea.split(':', 1)
                dependencias.append({'tipo': 'normal', 'clave': partes[0].strip(), 'valor': partes[1].strip()})
            elif linea.strip():
                dependencias.append({'tipo': 'colspan', 'valor': linea.strip()})

    # Estructuramos el Changelog para Jinja2
    changelog = None
    if 'Changelog' in etiquetas:
        lineas = etiquetas["Changelog"].strip().split('\n')
        if lineas:
            cabeceras = re.split(r'\s{2,}', lineas[0].strip())
            filas = []
            for linea in lineas[1:]:
                if linea.strip():
                    columnas = re.split(r'\s{2,}', linea.strip())
                    columnas += [''] * (len(cabeceras) - len(columnas)) # Relleno de seguridad
                    filas.append(columnas)
            changelog = {"cabeceras": cabeceras, "filas": filas}

    # Variables
    variables = []
    for bloque in re.finditer(r'(VAR_INPUT|VAR_OUTPUT|VAR_IN_OUT|VAR_TEMP|VAR)(.*?)(?:END_VAR)', contenido, re.DOTALL):
        tipo_seccion = bloque.group(1)
        for linea in re.finditer(r'^\s*([a-zA-Z0-9_]+)\s*:\s*([^;]+);\s*(?://\s*(.*))?', bloque.group(2), re.MULTILINE):
            variables.append({'seccion': tipo_seccion, 'nombre': linea.group(1), 'tipo': linea.group(2), 'descripcion': linea.group(3).strip() if linea.group(3) else ''})

    # Regiones
    regiones, pila, doc_pendiente = [], [], "Sin documentación específica."
    patron_tokens = r'(?P<doc>///\s*<RegionDoc>\s*\(\*(?P<texto_doc>.*?)\*\)\s*///\s*</RegionDoc>)|(?P<region>^[ \t]*REGION\s+(?P<nombre_region>[^\n\r]+))|(?P<endregion>^[ \t]*END_REGION)'
    for match in re.finditer(patron_tokens, contenido, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE):
        if match.group('doc'):
            doc_pendiente = match.group('texto_doc').strip()
        elif match.group('region'):
            nueva_region = {'doc': doc_pendiente, 'nombre': match.group('nombre_region').strip(), 'nivel': len(pila) + 1, 'start_idx': match.end(), 'hijos': [], 'codigo': ''}
            pila.append(nueva_region)
            regiones.append(nueva_region)
            doc_pendiente = "Sin documentación específica."
        elif match.group('endregion') and pila:
            region_cerrada = pila.pop()
            region_cerrada['codigo'] = contenido[region_cerrada['start_idx']:match.start()].strip()
            if pila: pila[-1]['hijos'].append(region_cerrada['nombre'])

    return nombre_bloque, etiquetas, dependencias, changelog, variables, regiones, contenido

def obtener_menu_secciones(etiquetas, variables, regiones, contenido_original):
    """Devuelve los apartados que irán al árbol de navegación izquierdo."""
    secciones = []
    if 'Summary' in etiquetas: secciones.append({"id": "descripcion", "titulo": "Descripción General", "nivel": 2})
    if 'Requires' in etiquetas: secciones.append({"id": "dependencias", "titulo": "Dependencias", "nivel": 2})
    if 'Changelog' in etiquetas: secciones.append({"id": "changelog", "titulo": "Historial de Cambios", "nivel": 2})
    if variables: secciones.append({"id": "interfaz", "titulo": "Interfaz de Variables", "nivel": 2})
    
    for i, reg in enumerate(regiones):
        secciones.append({"id": f"region_{i}", "titulo": f"Lógica: {reg['nombre']}", "nivel": reg['nivel'] + 1})
        
    if contenido_original: secciones.append({"id": "codigo_fuente", "titulo": "Código Fuente Completo", "nivel": 2})
    return secciones