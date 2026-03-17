import os
import sys
import shutil
from jinja2 import Environment, FileSystemLoader

def obtener_ruta_base():
    """
    Obtiene la ruta absoluta del proyecto. 
    Es VITAL para que PyInstaller encuentre las carpetas estáticas al compilar el .exe.
    """
    if getattr(sys, 'frozen', False):
        # Si se ejecuta como un ejecutable (.exe), usa la carpeta temporal de PyInstaller
        return sys._MEIPASS
    else:
        # Si se ejecuta como script (.py), usa la ruta de este mismo archivo
        return os.path.dirname(os.path.abspath(__file__))

def configurar_jinja():
    """Conecta Jinja2 con nuestra carpeta de plantillas."""
    ruta_base = obtener_ruta_base()
    ruta_templates = os.path.join(ruta_base, 'templates')
    
    # Creamos el entorno de plantillas
    return Environment(loader=FileSystemLoader(ruta_templates))

def copiar_estaticos(ruta_destino):
    """Copia la carpeta CSS e imágenes a la ruta de generación de la ayuda."""
    ruta_base = obtener_ruta_base()
    
    # Rutas de origen en nuestro proyecto
    ruta_css_origen = os.path.join(ruta_base, 'static', 'css')
    
    # Rutas de destino donde el usuario quiere guardar la ayuda
    ruta_css_destino = os.path.join(ruta_destino, 'css')
    ruta_img_destino = os.path.join(ruta_destino, 'img')
    ruta_manual_destino = os.path.join(ruta_destino, 'manual')
    ruta_bloques_destino = os.path.join(ruta_destino, 'bloques')
    
    # 1. Creamos todas las carpetas necesarias en el destino
    for carpeta in [ruta_css_destino, ruta_img_destino, ruta_manual_destino, ruta_bloques_destino]:
        os.makedirs(carpeta, exist_ok=True)
        
    # 2. Copiamos los archivos estáticos reales (como el custom.css)
    archivo_css_origen = os.path.join(ruta_css_origen, 'custom.css')
    if os.path.exists(archivo_css_origen):
        shutil.copy(archivo_css_origen, ruta_css_destino)

def renderizar_pagina(titulo, contenido_html, ruta_guardado):
    """Coge la plantilla genérica, le inyecta el contenido y la guarda en el disco."""
    env = configurar_jinja()
    plantilla = env.get_template('layout_page.html')
    
    # Inyectamos las variables a los "comodines" de la plantilla
    html_final = plantilla.render(
        titulo_pagina=titulo,
        contenido=contenido_html
    )
    
    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(html_final)

def renderizar_index(manual_html, bloques_html, pagina_inicio, ruta_guardado):
    """Coge la plantilla del menú principal, inyecta los árboles de navegación y la guarda."""
    env = configurar_jinja()
    plantilla = env.get_template('layout_index.html')
    
    html_final = plantilla.render(
        manual_html=manual_html,
        bloques_html=bloques_html,
        pagina_inicio=pagina_inicio
    )
    
    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(html_final)

def renderizar_bloque_scl(nombre_bloque, etiquetas, dependencias, changelog, variables, regiones, contenido_original, ruta_guardado):
    """Carga los datos de Siemens en su plantilla y la envuelve en el layout de página."""
    env = configurar_jinja()
    plantilla_scl = env.get_template('template_scl.html')
    plantilla_base = env.get_template('layout_page.html')
    
    # 1. Rellenamos las cajas SCL
    html_interior = plantilla_scl.render(
        nombre_bloque=nombre_bloque,
        etiquetas=etiquetas,
        dependencias=dependencias,
        changelog=changelog,
        variables=variables,
        regiones=regiones,
        contenido_original=contenido_original
    )
    
    # 2. Metemos todo ese bloque dentro de la página con menú, css, etc.
    html_final = plantilla_base.render(
        titulo_pagina=nombre_bloque,
        contenido=html_interior
    )
    
    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(html_final)

def construir_arbol_manual(capitulos_manual):
    """Genera el HTML interactivo del menú lateral para el Word."""
    menu_manual = []
    for cap in capitulos_manual:
        menu_manual.append({"enlace": f'manual/{cap["archivo"]}', "titulo": cap["titulo"], "nivel": cap["nivel"]})
        for sub in cap.get("subsecciones", []):
            menu_manual.append({"enlace": f'manual/{cap["archivo"]}#{sub["id"]}', "titulo": sub["titulo"], "nivel": sub["nivel"]})

    manual_html = ""
    nivel_actual = 1
    for i, item in enumerate(menu_manual):
        nivel = item["nivel"]
        tiene_hijos = (i + 1 < len(menu_manual) and menu_manual[i+1]["nivel"] > nivel)
        if nivel < nivel_actual:
            for _ in range(nivel_actual - nivel): manual_html += "</ul></li>\n"
            nivel_actual = nivel
            
        pad_left = 10 + ((nivel - 1) * 22)
        if nivel == 1: estilo = "font-weight: bold; font-size: 13.5px; color: #005c8a;"
        elif nivel == 2: estilo = "font-weight: 500; font-size: 13px; color: #333;"
        else: estilo = "font-weight: normal; font-size: 12.5px; color: #555; font-style: italic;"
            
        btn = '<div class="toggle-btn" onclick="toggleMenu(this)">▼</div>' if tiene_hijos else '<div class="toggle-spacer"></div>'
        manual_html += f'<li><div class="menu-item" style="padding-left: {pad_left}px;">{btn}<a class="menu-link" style="{estilo}" href="{item["enlace"]}" target="visor">{item["titulo"]}</a></div>\n'
        
        if tiene_hijos:
            manual_html += '<ul class="nested" style="display: none;">\n'
            nivel_actual += 1
        else:
            manual_html += '</li>\n'
    for _ in range(nivel_actual - 1): manual_html += "</ul></li>\n"
    return manual_html

def construir_arbol_bloques(bloques_info):
    """Genera el HTML interactivo del menú lateral para los bloques SCL."""
    bloques_html = ""
    if not bloques_info:
        return '<li><div class="menu-item" style="padding-left: 10px;"><div class="toggle-spacer"></div><i class="menu-link" style="color:#999; font-size: 13px;">No hay bloques documentados</i></div></li>'
        
    for bloque in bloques_info:
        tiene_secciones = len(bloque["secciones"]) > 0
        btn_bloque = '<div class="toggle-btn" onclick="toggleMenu(this)">▼</div>' if tiene_secciones else '<div class="toggle-spacer"></div>'
        bloques_html += f'<li><div class="menu-item" style="padding-left: 10px;">{btn_bloque}<a class="menu-link" style="font-weight: bold; font-size: 13.5px; color: #005c8a;" href="bloques/{bloque["archivo"]}" target="visor">{bloque["nombre"]}</a></div>\n'
        
        if tiene_secciones:
            bloques_html += '<ul class="nested" style="display: none;">\n'
            nivel_actual = 2
            for i, sec in enumerate(bloque["secciones"]):
                nivel = sec["nivel"]
                tiene_hijos = (i + 1 < len(bloque["secciones"]) and bloque["secciones"][i+1]["nivel"] > nivel)
                if nivel < nivel_actual:
                    for _ in range(nivel_actual - nivel): bloques_html += "</ul></li>\n"
                    nivel_actual = nivel
                    
                pad_left = 10 + ((nivel - 1) * 22)
                if nivel == 2: estilo = "font-weight: normal; font-size: 12.5px; color: #444;"
                else: estilo = "font-weight: normal; font-size: 12px; color: #666; font-style: italic;"
                
                btn_sec = '<div class="toggle-btn" onclick="toggleMenu(this)">▼</div>' if tiene_hijos else '<div class="toggle-spacer"></div>'
                bloques_html += f'<li><div class="menu-item" style="padding-left: {pad_left}px;">{btn_sec}<a class="menu-link" style="{estilo}" href="bloques/{bloque["archivo"]}#{sec["id"]}" target="visor">{sec["titulo"]}</a></div>\n'
                
                if tiene_hijos:
                    bloques_html += '<ul class="nested" style="display: none;">\n'
                    nivel_actual += 1
                else:
                    bloques_html += '</li>\n'
            for _ in range(nivel_actual - 2): bloques_html += "</ul></li>\n"
            bloques_html += '</ul>\n'
        bloques_html += '</li>\n'
    return bloques_html