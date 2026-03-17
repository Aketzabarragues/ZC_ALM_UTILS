import os
import ui_dialogs
import core_parser_word
import core_parser_scl
import html_renderer
from tkinter import filedialog

def seleccionar_carpeta_scl():
    return filedialog.askdirectory(title="3. (Opcional) Selecciona la carpeta con los fuentes SCL exportados")

def main():
    ui_dialogs.inicializar_ui()
    
    print("=================================================")
    print(" ZCALM - GENERADOR DE DOCUMENTACIÓN v2.0 (FINAL) ")
    print("=================================================")

    ruta_word = ui_dialogs.seleccionar_archivo_origen()
    if not ruta_word: return
    
    ruta_scl = seleccionar_carpeta_scl()
    
    ruta_destino = ui_dialogs.seleccionar_carpeta_destino()
    if not ruta_destino: return

    try:
        print(f"\n1. Preparando entorno en: {ruta_destino}")
        html_renderer.copiar_estaticos(ruta_destino)

        print(f"2. Procesando manual de Word...")
        capitulos = core_parser_word.procesar_word(ruta_word, ruta_destino)
        
        # Renderizar cada capítulo del Word
        for cap in capitulos:
            ruta_guardado = os.path.join(ruta_destino, 'manual', cap["archivo"])
            html_renderer.renderizar_pagina(cap["titulo"], cap["contenido"], ruta_guardado)

        print(f"3. Procesando bloques SCL...")
        bloques_info = []
        if ruta_scl and os.path.exists(ruta_scl):
            archivos_scl = [f for f in os.listdir(ruta_scl) if f.lower().endswith('.scl')]
            for archivo in archivos_scl:
                ruta_completa = os.path.join(ruta_scl, archivo)
                
                # Extraemos datos
                nombre, etiquetas, dependencias, changelog, variables, regiones, cont_orig = core_parser_scl.parsear_scl(ruta_completa)
                
                # Renderizamos la plantilla Jinja2
                ruta_guardado = os.path.join(ruta_destino, 'bloques', f"{nombre}.html")
                html_renderer.renderizar_bloque_scl(nombre, etiquetas, dependencias, changelog, variables, regiones, cont_orig, ruta_guardado)
                
                # Guardamos su estructura para el menú izquierdo
                secciones = core_parser_scl.obtener_menu_secciones(etiquetas, variables, regiones, cont_orig)
                bloques_info.append({"nombre": nombre, "archivo": f"{nombre}.html", "secciones": secciones})
                
            print(f"   -> ¡{len(archivos_scl)} bloques procesados con éxito!")

        print(f"4. Generando Índice de Navegación Maestro...")
        manual_html = html_renderer.construir_arbol_manual(capitulos)
        bloques_html = html_renderer.construir_arbol_bloques(bloques_info)
        pagina_inicio = f"manual/{capitulos[0]['archivo']}" if capitulos else "inicio.html"
        
        html_renderer.renderizar_index(manual_html, bloques_html, pagina_inicio, os.path.join(ruta_destino, 'index.html'))

        ui_dialogs.mostrar_exito(f"Ayuda corporativa generada con éxito en:\n{ruta_destino}")

    except Exception as e:
        import traceback
        traceback.print_exc()
        ui_dialogs.mostrar_error(f"Error crítico durante la generación:\n{e}")

if __name__ == "__main__":
    main()