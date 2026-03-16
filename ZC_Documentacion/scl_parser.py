import os
import re
import html 

def parsear_scl(ruta_archivo):
    """Lee un archivo .scl y extrae toda la documentación y lógica."""
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()

    match_nombre = re.search(r'(FUNCTION|FUNCTION_BLOCK|DATA_BLOCK)\s+"([^"]+)"', contenido)
    nombre_bloque = match_nombre.group(2) if match_nombre else os.path.basename(ruta_archivo).replace('.scl', '')

    etiquetas = {}
    matches_tags = re.finditer(r'///\s*<(\w+)>\s*\(\*(.*?)\*\)\s*///\s*</\1>', contenido, re.DOTALL)
    for match in matches_tags:
        nombre_tag = match.group(1)
        if nombre_tag != 'RegionDoc':
            etiquetas[nombre_tag] = match.group(2).strip()

    variables = []
    bloques_var = re.finditer(r'(VAR_INPUT|VAR_OUTPUT|VAR_IN_OUT|VAR_TEMP|VAR)(.*?)(?:END_VAR)', contenido, re.DOTALL)
    for bloque in bloques_var:
        tipo_seccion = bloque.group(1)
        contenido_var = bloque.group(2)
        lineas_var = re.finditer(r'^\s*([a-zA-Z0-9_]+)\s*:\s*([^;]+);\s*(?://\s*(.*))?', contenido_var, re.MULTILINE)
        for linea in lineas_var:
            variables.append({'seccion': tipo_seccion, 'nombre': linea.group(1), 'tipo': linea.group(2), 'descripcion': linea.group(3).strip() if linea.group(3) else ''})

    regiones = []
    pila = []
    doc_pendiente = "Sin documentación específica."

    patron_tokens = r'(?P<doc>///\s*<RegionDoc>\s*\(\*(?P<texto_doc>.*?)\*\)\s*///\s*</RegionDoc>)|(?P<region>^[ \t]*REGION\s+(?P<nombre_region>[^\n\r]+))|(?P<endregion>^[ \t]*END_REGION)'
    
    for match in re.finditer(patron_tokens, contenido, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE):
        if match.group('doc'):
            doc_pendiente = match.group('texto_doc').strip()
        elif match.group('region'):
            nivel = len(pila) + 1
            nueva_region = {
                'doc': doc_pendiente,
                'nombre': match.group('nombre_region').strip(),
                'nivel': nivel,
                'start_idx': match.end(),
                'hijos': [], 
                'codigo': ''
            }
            pila.append(nueva_region)
            regiones.append(nueva_region)
            doc_pendiente = "Sin documentación específica."
        elif match.group('endregion'):
            if pila:
                region_cerrada = pila.pop()
                region_cerrada['codigo'] = contenido[region_cerrada['start_idx']:match.start()].strip()
                
                if pila:
                    pila[-1]['hijos'].append(region_cerrada['nombre'])

    return nombre_bloque, etiquetas, variables, regiones, contenido

def generar_html_bloque(nombre_bloque, etiquetas, variables, regiones, contenido_original, ruta_destino):
    secciones = [] 
    
    contenido_html = f'<h1 class="doc-title">{nombre_bloque}</h1>\n'
    
    # 1. DESCRIPCIÓN GENERAL (Nivel 2)
    if 'Summary' in etiquetas:
        secciones.append({"id": "descripcion", "titulo": "Descripción General", "nivel": 2})
        contenido_html += f'<div class="doc-section" id="descripcion">\n<h3>Descripción General</h3>\n<pre style="font-family: inherit; white-space: pre-wrap; margin:0; line-height: 1.5;">{etiquetas["Summary"]}</pre>\n'
        if 'Remarks' in etiquetas:
            contenido_html += f'<div style="margin-top:15px; padding:12px; background:#f8fafc; border-left:4px solid #94a3b8; border-radius: 4px;"><pre style="font-family: inherit; white-space: pre-wrap; margin:0; line-height: 1.5;"><strong style="color:#334155;">Notas y Restricciones:</strong>\n{etiquetas["Remarks"]}</pre></div>\n'
        contenido_html += '</div>\n'

    # 2. DEPENDENCIAS (Nivel 2)
    if 'Requires' in etiquetas:
        secciones.append({"id": "dependencias", "titulo": "Dependencias", "nivel": 2})
        contenido_html += '<div class="doc-section" id="dependencias">\n<h3>Dependencias</h3>\n<table class="doc-table">\n'
        contenido_html += '<tr><th>Tipo de Elemento</th><th>Nombre / Bloques</th></tr>\n'
        lineas_req = etiquetas["Requires"].strip().split('\n')
        for linea in lineas_req:
            if ':' in linea:
                partes = linea.split(':', 1) 
                contenido_html += f'<tr><td><strong>{partes[0].strip()}</strong></td><td>{partes[1].strip()}</td></tr>\n'
            elif linea.strip():
                contenido_html += f'<tr><td colspan="2">{linea.strip()}</td></tr>\n'
        contenido_html += '</table>\n</div>\n'

    # 3. HISTORIAL DE CAMBIOS (Nivel 2)
    if 'Changelog' in etiquetas:
        secciones.append({"id": "changelog", "titulo": "Historial de Cambios", "nivel": 2})
        contenido_html += '<div class="doc-section" id="changelog">\n<h3>Historial de Cambios (Changelog)</h3>\n<table class="doc-table">\n'
        lineas_change = etiquetas["Changelog"].strip().split('\n')
        if lineas_change:
            cabeceras = re.split(r'\s{2,}', lineas_change[0].strip())
            contenido_html += '<tr>'
            for cab in cabeceras: contenido_html += f'<th>{cab}</th>'
            contenido_html += '</tr>\n'
            for linea in lineas_change[1:]:
                if linea.strip():
                    columnas = re.split(r'\s{2,}', linea.strip())
                    contenido_html += '<tr>'
                    for col in columnas: contenido_html += f'<td>{col}</td>'
                    for _ in range(len(cabeceras) - len(columnas)): contenido_html += '<td></td>'
                    contenido_html += '</tr>\n'
        contenido_html += '</table>\n</div>\n'

    # 4. INTERFAZ DE VARIABLES (Nivel 2)
    if variables:
        secciones.append({"id": "interfaz", "titulo": "Interfaz de Variables", "nivel": 2})
        contenido_html += '<div class="doc-section" id="interfaz">\n<h3>Interfaz de Variables</h3>\n<table class="doc-table">\n'
        contenido_html += '<tr><th>Sección</th><th>Nombre</th><th>Tipo de Dato</th><th>Descripción</th></tr>\n'
        for var in variables:
            contenido_html += f'<tr><td><span style="font-size:11px; color:#666;">{var["seccion"]}</span></td><td><strong>{var["nombre"]}</strong></td><td>{var["tipo"]}</td><td>{var["descripcion"]}</td></tr>\n'
        contenido_html += '</table>\n</div>\n'

    # 5. REGIONES (Nivel dinámico 2, 3, 4...)
    nivel_previo = 0
    for i, reg in enumerate(regiones):
        id_region = f"region_{i}"
        
        # MAGIA AQUÍ: Añadimos la sección con el nivel real para que doc_builder la anide, sin flechas raras
        nivel_real = reg['nivel'] + 1 
        secciones.append({"id": id_region, "titulo": f"Lógica: {reg['nombre']}", "nivel": nivel_real})
        
        if reg['nivel'] <= nivel_previo:
            cierres = nivel_previo - reg['nivel'] + 1
            for _ in range(cierres):
                contenido_html += '</div>\n'
                
        if reg['nivel'] == 1:
            contenido_html += f'<div class="doc-section" id="{id_region}">\n'
            contenido_html += f'<h3>Lógica: {reg["nombre"]}</h3>\n'
        else:
            contenido_html += f'<div id="{id_region}" style="background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; margin-top: 20px; border-radius: 6px;">\n'
            contenido_html += f'<h4 style="color: #005c8a; margin-top:0; font-size: 15px; border-bottom: 1px dashed #cbd5e1; padding-bottom: 5px; margin-bottom: 10px;">↳ Sub-lógica: {reg["nombre"]}</h4>\n'
            
        if reg["doc"] == "Sin documentación específica.":
            contenido_html += f'<p style="color:#999; font-style:italic; margin-bottom:15px;">{reg["doc"]}</p>\n'
        else:
            contenido_html += f'<pre style="font-family: inherit; white-space: pre-wrap; margin:0; padding-bottom: 15px; color: #334155; line-height: 1.5;">{reg["doc"]}</pre>\n'
            
        if len(reg['hijos']) == 0:
            contenido_html += f'<pre class="scl-code" style="margin-bottom: 0;">REGION {reg["nombre"]}\n{reg["codigo"]}\nEND_REGION</pre>\n'
        else:
            contenido_html += f'<p style="color:#64748b; font-size: 13px; margin: 0; font-style: italic;">(El detalle del código SCL se encuentra desglosado en las sub-regiones inferiores).</p>\n'
        
        nivel_previo = reg['nivel']

    if nivel_previo > 0:
        for _ in range(nivel_previo):
            contenido_html += '</div>\n'

    # 6. CÓDIGO FUENTE COMPLETO (Nivel 2)
    if contenido_original:
        secciones.append({"id": "codigo_fuente", "titulo": "Código Fuente Completo", "nivel": 2})
        contenido_html += f'<div class="doc-section" id="codigo_fuente" style="margin-top: 40px; border-top: 4px solid #005c8a;">\n'
        contenido_html += f'<h3>Código Fuente Completo</h3>\n'
        codigo_seguro = html.escape(contenido_original)
        contenido_html += f'<pre class="scl-code" style="max-height: 600px; overflow-y: auto;">{codigo_seguro}</pre>\n'
        contenido_html += f'</div>\n'

    html_final = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../css/custom.css">
</head>
<body>
    <div class="page-wrapper">
        <div class="page-content">
            {contenido_html}
            <div style="height: 500px;"></div>
        </div>
    </div>
</body>
</html>"""

    ruta_guardado = os.path.join(ruta_destino, 'bloques', f"{nombre_bloque}.html")
    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(html_final)
        
    return secciones