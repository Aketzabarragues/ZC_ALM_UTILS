"""
Motor de Renderizado HTML (View Layer).

Este módulo gestiona la transformación de las estructuras de datos en memoria (DTOs)
en vistas HTML estáticas utilizando el motor de plantillas Jinja2.
Se encarga del aprovisionamiento de recursos estáticos, la composición de layouts 
y la generación algorítmica de los árboles de navegación del Document Object Model (DOM).
"""

import os
import sys
import shutil
from jinja2 import Environment, FileSystemLoader
from core import core_logger as log


def obtener_ruta_base():
    """
    Resuelve la ruta absoluta del directorio de ejecución.
    Apunta siempre a la RAÍZ del proyecto (ZC_Documentacion).
    """
    if getattr(sys, 'frozen', False):
        # Si es un .exe, devuelve la carpeta temporal raíz _MEIPASS
        return sys._MEIPASS

    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(directorio_actual, '..'))

def configurar_jinja():
    """
    Inicializa y configura el entorno del motor de plantillas Jinja2.
    
    Returns:
        Environment: Instancia de Jinja2 enlazada al directorio estático de plantillas.
    """
    ruta_templates = os.path.join(obtener_ruta_base(), 'ui', 'templates')
    return Environment(loader=FileSystemLoader(ruta_templates))


def copiar_estaticos(ruta_destino):
    """
    Aprovisiona el directorio de salida inicializando la topología de carpetas
    e inyectando los recursos estáticos compartidos (Hojas de estilo e Imágenes).
    
    Args:
        ruta_destino (str): Directorio raíz donde se desplegará la documentación web.
    """
    log.info(f"Desplegando topología de carpetas en: {ruta_destino}")
    ruta_base = obtener_ruta_base()
    
    ruta_css_destino = os.path.join(ruta_destino, 'css')
    ruta_img_destino = os.path.join(ruta_destino, 'img')
    
    # exist_ok=True garantiza la idempotencia (no falla si la carpeta ya existe)
    os.makedirs(ruta_css_destino, exist_ok=True)
    os.makedirs(ruta_img_destino, exist_ok=True)
    os.makedirs(os.path.join(ruta_destino, 'manual'), exist_ok=True)
    os.makedirs(os.path.join(ruta_destino, 'bloques'), exist_ok=True)
    
    # Despliegue de CSS personalizado
    archivo_css_origen = os.path.join(ruta_base, 'static', 'css', 'custom.css')
    if os.path.exists(archivo_css_origen):
        shutil.copy(archivo_css_origen, ruta_css_destino)
        
    # Despliegue masivo de recursos gráficos (Logos, iconos, etc.)
    ruta_img_origen = os.path.join(ruta_base, 'static', 'img')
    if os.path.exists(ruta_img_origen):
        for archivo in os.listdir(ruta_img_origen):
            shutil.copy(os.path.join(ruta_img_origen, archivo), ruta_img_destino)
        log.debug("Aprovisionamiento de recursos estáticos (CSS/IMG) finalizado.")


def renderizar_pagina(titulo, contenido_html, ruta_guardado):
    """
    Renderiza una vista genérica (típicamente capítulos procesados del Manual Word).
    """
    env = configurar_jinja()
    plantilla = env.get_template('layout_page.html')
    html_final = plantilla.render(titulo_pagina=titulo, contenido=contenido_html)
    
    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(html_final)


def renderizar_bloque_scl(datos_bloque, ruta_guardado):
    """
    Renderiza la vista detallada de un bloque de código (FC/FB).
    
    Utiliza un patrón de composición de plantillas: procesa primero el DOM interno 
    (template_scl) con las propiedades SCL, y luego lo inyecta como contenido 
    en el contenedor maestro (layout_page).
    
    Args:
        datos_bloque (dict): Diccionario DTO con la estructura del bloque SCL.
        ruta_guardado (str): Path de escritura del archivo HTML resultante.
    """
    log.debug(f"Renderizando DOM estático para el bloque SCL: {datos_bloque['nombre_bloque']}")
    env = configurar_jinja()
    plantilla_scl = env.get_template('template_scl.html')
    plantilla_base = env.get_template('layout_page.html')
    
    # 1. Composición del componente interno desempaquetando el diccionario (Kwargs)
    html_interior = plantilla_scl.render(**datos_bloque)
    
    # 2. Inyección en el Layout Padre
    html_final = plantilla_base.render(titulo_pagina=datos_bloque['nombre_bloque'], contenido=html_interior)
    
    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(html_final)


def renderizar_datos(bloque, ruta_salida):
    """
    Renderiza la vista detallada de una estructura de datos (DB/UDT).
    Aplica el mismo patrón de composición que los bloques SCL pero usando template_data.
    """
    log.debug(f"Renderizando DOM estático para la estructura de datos: {bloque['nombre_bloque']}")
    env = configurar_jinja() 
    
    plantilla_datos = env.get_template('template_data.html')
    plantilla_base = env.get_template('layout_page.html')
    
    html_interior = plantilla_datos.render(bloque=bloque)
    html_final = plantilla_base.render(titulo_pagina=bloque['nombre_bloque'], contenido=html_interior)
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html_final)


def construir_arbol_manual(capitulos_manual):
    """
    Genera el HTML en crudo para el índice lateral interactivo del manual (Word).
    
    Implementa un algoritmo de control de profundidad que rastrea los niveles de 
    jerarquía (H1, H2, H3) y gestiona de forma segura la apertura y cierre de 
    listas anidadas (<ul>, <li>) en el DOM.
    """
    menu_manual = []
    
    # Indexación secuencial de los capítulos y subsecciones
    for cap in capitulos_manual:
        menu_manual.append({"enlace": f'manual/{cap["archivo"]}', "titulo": cap["titulo"], "nivel": cap["nivel"]})
        for sub in cap.get("subsecciones", []):
            menu_manual.append({"enlace": f'manual/{cap["archivo"]}#{sub["id"]}', "titulo": sub["titulo"], "nivel": sub["nivel"]})

    manual_html = ""
    nivel_actual = 1
    
    # Evaluación de estado para inyección de nodos en el DOM
    for i, item in enumerate(menu_manual):
        nivel = item["nivel"]
        tiene_hijos = (i + 1 < len(menu_manual) and menu_manual[i+1]["nivel"] > nivel)
        
        # Compensación de cierres de etiquetas al ascender en el árbol
        if nivel < nivel_actual:
            for _ in range(nivel_actual - nivel): 
                manual_html += "</ul></li>\n"
            nivel_actual = nivel
            
        pad_left = 5 + ((nivel - 1) * 15)
        clase_nivel = f"level-{nivel}"
            
        btn = '<div class="toggle-btn" onclick="toggleMenu(this)"></div>' if tiene_hijos else '<div class="toggle-spacer"></div>'
        manual_html += f'<li><div class="menu-item" style="padding-left: {pad_left}px;">{btn}<a class="menu-link {clase_nivel}" href="{item["enlace"]}" target="visor">{item["titulo"]}</a></div>\n'
        
        # Apertura de nodo anidado si procede
        if tiene_hijos:
            manual_html += '<ul class="nested" style="display: none;">\n'
            nivel_actual += 1
        else:
            manual_html += '</li>\n'
            
    # Clausura segura de todos los niveles residuales al finalizar el bucle
    for _ in range(nivel_actual - 1): 
        manual_html += "</ul></li>\n"
        
    return manual_html


def construir_arbol_bloques(bloques_info):
    """
    Genera el HTML en crudo para el índice lateral interactivo de código y datos.
    Implementa la misma lógica de jerarquía algorítmica que construir_arbol_manual().
    """
    bloques_html = ""
    
    if not bloques_info:
        return ('<li><div class="menu-item" style="padding-left: 10px;">'
                '<div class="toggle-spacer"></div>'
                '<i class="menu-link" style="color:#999; font-size: 13px;">No hay recursos documentados</i>'
                '</div></li>')
        
    for bloque in bloques_info:
        tiene_secciones = len(bloque["secciones"]) > 0
        btn_bloque = '<div class="toggle-btn" onclick="toggleMenu(this)"></div>' if tiene_secciones else '<div class="toggle-spacer"></div>'
        
        # Inserción del nodo raíz del bloque (Siempre de nivel 1 en la vista)
        bloques_html += f'<li><div class="menu-item" style="padding-left: 5px;">{btn_bloque}<a class="menu-link level-1" href="bloques/{bloque["archivo"]}" target="visor">{bloque["nombre"]}</a></div>\n'
        
        if tiene_secciones:
            bloques_html += '<ul class="nested" style="display: none;">\n'
            nivel_actual = 1 
            
            for i, sec in enumerate(bloque["secciones"]):
                nivel = sec["nivel"]
                tiene_hijos = (i + 1 < len(bloque["secciones"]) and bloque["secciones"][i+1]["nivel"] > nivel)
                
                # Compensación de cierres
                if nivel < nivel_actual:
                    for _ in range(nivel_actual - nivel): 
                        bloques_html += "</ul></li>\n"
                    nivel_actual = nivel
                    
                # Incremento visual del nivel para diferenciar de la raíz del bloque
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
                    
            # Clausura de seguridad de subsecciones
            for _ in range(nivel_actual - 1): 
                bloques_html += "</ul></li>\n"
            bloques_html += '</ul>\n'
            
        bloques_html += '</li>\n'
        
    return bloques_html


def renderizar_index(manual_html, funciones_html, datos_html, pagina_inicio, ruta_guardado):
    """
    Renderiza la vista principal (Index.html) que aloja el menú interactivo lateral 
    y el IFrame contenedor.
    
    Args:
        manual_html (str): Árbol DOM del manual pre-procesado.
        funciones_html (str): Árbol DOM de bloques SCL pre-procesado.
        datos_html (str): Árbol DOM de estructuras de datos pre-procesado.
        pagina_inicio (str): Ruta predeterminada a cargar en el IFrame al inicio.
        ruta_guardado (str): Path absoluto de escritura del archivo principal.
    """
    log.info("Renderizando contenedor maestro (index.html)...")
    env = configurar_jinja()
    plantilla = env.get_template('layout_index.html')
    
    html_final = plantilla.render(
        manual_html=manual_html, 
        funciones_html=funciones_html, 
        datos_html=datos_html,
        pagina_inicio=pagina_inicio
    )
    
    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(html_final)