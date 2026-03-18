import os
import sys
import shutil
from jinja2 import Environment, FileSystemLoader
import core_logger as log

def obtener_ruta_base():
    """Ruta absoluta compatible con el futuro .exe de PyInstaller."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def configurar_jinja():
    """Conecta con la carpeta /templates."""
    ruta_templates = os.path.join(obtener_ruta_base(), 'templates')
    return Environment(loader=FileSystemLoader(ruta_templates))

def copiar_estaticos(ruta_destino):
    """Crea las carpetas base y copia el CSS y las imágenes estáticas."""
    log.info(f"Creando estructura de carpetas en destino: {ruta_destino}")
    ruta_base = obtener_ruta_base()
    
    ruta_css_destino = os.path.join(ruta_destino, 'css')
    ruta_img_destino = os.path.join(ruta_destino, 'img')
    os.makedirs(ruta_css_destino, exist_ok=True)
    os.makedirs(ruta_img_destino, exist_ok=True)
    os.makedirs(os.path.join(ruta_destino, 'manual'), exist_ok=True)
    os.makedirs(os.path.join(ruta_destino, 'bloques'), exist_ok=True)
    
    # Copiar CSS
    archivo_css_origen = os.path.join(ruta_base, 'static', 'css', 'custom.css')
    if os.path.exists(archivo_css_origen):
        shutil.copy(archivo_css_origen, ruta_css_destino)
        
    # Copiar Logo y otras imágenes estáticas
    ruta_img_origen = os.path.join(ruta_base, 'static', 'img')
    if os.path.exists(ruta_img_origen):
        for archivo in os.listdir(ruta_img_origen):
            shutil.copy(os.path.join(ruta_img_origen, archivo), ruta_img_destino)
        log.debug("Archivos estáticos (CSS/IMG) copiados correctamente.")

def renderizar_pagina(titulo, contenido_html, ruta_guardado):
    """Renderiza páginas genéricas (como las del manual de Word)."""
    env = configurar_jinja()
    plantilla = env.get_template('layout_page.html')
    html_final = plantilla.render(titulo_pagina=titulo, contenido=contenido_html)
    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(html_final)

def renderizar_bloque_scl(datos_bloque, ruta_guardado):
    """Renderiza un bloque SCL usando las plantillas de Jinja2."""
    log.debug(f"Renderizando HTML para el bloque: {datos_bloque['nombre_bloque']}")
    env = configurar_jinja()
    plantilla_scl = env.get_template('template_scl.html')
    plantilla_base = env.get_template('layout_page.html')
    
    # 1. Rellenamos las cajas SCL (pasamos todo el diccionario de golpe)
    html_interior = plantilla_scl.render(**datos_bloque)
    
    # 2. Metemos las cajas en la página maestra
    html_final = plantilla_base.render(titulo_pagina=datos_bloque['nombre_bloque'], contenido=html_interior)
    
    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(html_final)

def renderizar_datos(bloque, ruta_salida):
    """
    Renderiza un bloque de datos (UDT o DB) integrándolo en la página maestra.
    """
    # IMPORTANTE: Asegúrate de que tienes "import core_logger as log" arriba en tu archivo
    log.debug(f"Renderizando HTML para el dato: {bloque['nombre_bloque']}")
    
    # Usamos tu función configurar_jinja() que ya tienes en html_renderer.py
    env = configurar_jinja() 
    
    plantilla_datos = env.get_template('template_data.html')
    plantilla_base = env.get_template('layout_page.html')
    
    # 1. Rellenamos la caja interior con la tabla de variables
    html_interior = plantilla_datos.render(bloque=bloque)
    
    # 2. Metemos la caja dentro de la página oficial
    html_final = plantilla_base.render(titulo_pagina=bloque['nombre_bloque'], contenido=html_interior)
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
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
            for _ in range(nivel_actual - nivel): 
                manual_html += "</ul></li>\n"
            nivel_actual = nivel
            
        pad_left = 5 + ((nivel - 1) * 15)
        clase_nivel = f"level-{nivel}"
            
        btn = '<div class="toggle-btn" onclick="toggleMenu(this)"></div>' if tiene_hijos else '<div class="toggle-spacer"></div>'
        manual_html += f'<li><div class="menu-item" style="padding-left: {pad_left}px;">{btn}<a class="menu-link {clase_nivel}" href="{item["enlace"]}" target="visor">{item["titulo"]}</a></div>\n'
        
        if tiene_hijos:
            manual_html += '<ul class="nested" style="display: none;">\n'
            nivel_actual += 1
        else:
            manual_html += '</li>\n'
            
    for _ in range(nivel_actual - 1): 
        manual_html += "</ul></li>\n"
    return manual_html

def construir_arbol_bloques(bloques_info):
    """Genera el HTML interactivo del menú lateral para los bloques SCL/DBs/UDTs."""
    bloques_html = ""
    if not bloques_info:
        return '<li><div class="menu-item" style="padding-left: 10px;"><div class="toggle-spacer"></div><i class="menu-link" style="color:#999; font-size: 13px;">No hay bloques documentados</i></div></li>'
        
    for bloque in bloques_info:
        tiene_secciones = len(bloque["secciones"]) > 0
        btn_bloque = '<div class="toggle-btn" onclick="toggleMenu(this)"></div>' if tiene_secciones else '<div class="toggle-spacer"></div>'
        
        # El bloque principal siempre es nivel 1
        bloques_html += f'<li><div class="menu-item" style="padding-left: 5px;">{btn_bloque}<a class="menu-link level-1" href="bloques/{bloque["archivo"]}" target="visor">{bloque["nombre"]}</a></div>\n'
        
        if tiene_secciones:
            bloques_html += '<ul class="nested" style="display: none;">\n'
            nivel_actual = 1 # Iniciamos el nivel relativo a las regiones
            
            for i, sec in enumerate(bloque["secciones"]):
                nivel = sec["nivel"]
                tiene_hijos = (i + 1 < len(bloque["secciones"]) and bloque["secciones"][i+1]["nivel"] > nivel)
                
                # Cierre correcto de etiquetas para no romper el HTML
                if nivel < nivel_actual:
                    for _ in range(nivel_actual - nivel): 
                        bloques_html += "</ul></li>\n"
                    nivel_actual = nivel
                    
                # El nivel visual en CSS es nivel+1 porque el bloque es el 1
                nivel_css = nivel + 1
                pad_left = 5 + ((nivel_css - 1) * 15)
                clase_nivel = f"level-{nivel_css}"
                
                btn_sec = '<div class="toggle-btn" onclick="toggleMenu(this)"></div>' if tiene_hijos else '<div class="toggle-spacer"></div>'
                bloques_html += f'<li><div class="menu-item" style="padding-left: {pad_left}px;">{btn_sec}<a class="menu-link {clase_nivel}" href="bloques/{bloque["archivo"]}#{sec["id"]}" target="visor">{sec["titulo"]}</a></div>\n'
                
                if tiene_hijos:
                    bloques_html += '<ul class="nested" style="display: none;">\n'
                    nivel_actual += 1
                else:
                    bloques_html += '</li>\n'
                    
            for _ in range(nivel_actual - 1): 
                bloques_html += "</ul></li>\n"
            bloques_html += '</ul>\n'
            
        bloques_html += '</li>\n'
    return bloques_html

def renderizar_index(manual_html, bloques_html, pagina_inicio, ruta_guardado):
    """Renderiza el menú lateral interactivo."""
    log.info("Renderizando index.html principal...")
    env = configurar_jinja()
    plantilla = env.get_template('layout_index.html')
    html_final = plantilla.render(manual_html=manual_html, bloques_html=bloques_html, pagina_inicio=pagina_inicio)
    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(html_final)