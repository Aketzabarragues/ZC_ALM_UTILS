import os
import ui_dialogs
import core_logger as log
import core_parser_word
import core_parser_scl
import core_linker
import html_renderer
from tkinter import filedialog

def seleccionar_carpeta_scl():
    return filedialog.askdirectory(title="3. (Opcional) Selecciona la carpeta con los fuentes SCL exportados")

def main():
    ui_dialogs.inicializar_ui()
    
    log.info("=================================================")
    log.info(" ZCALM - GENERADOR DE DOCUMENTACIÓN v3.0 (PRO)   ")
    log.info("=================================================")

    # -- INTERFAZ DE USUARIO --
    ruta_word = ui_dialogs.seleccionar_archivo_origen()
    if not ruta_word: return
    
    ruta_scl = seleccionar_carpeta_scl()
    
    ruta_destino = ui_dialogs.seleccionar_carpeta_destino()
    if not ruta_destino: return

    try:
        log.info(f"Iniciando proceso en la ruta destino: {ruta_destino}")
        html_renderer.copiar_estaticos(ruta_destino)

        # -- FASE 1 y 2: EXTRAER DATOS (WORD) --
        capitulos_word = core_parser_word.procesar_word(ruta_word, ruta_destino)

        # -- FASE 1 y 2: EXTRAER DATOS (SCL) --
        bloques_scl = []
        if ruta_scl and os.path.exists(ruta_scl):
            log.info(f"Escaneando carpeta SCL: {ruta_scl}")
            archivos_scl = [f for f in os.listdir(ruta_scl) if f.lower().endswith('.scl')]
            
            for archivo in archivos_scl:
                ruta_completa = os.path.join(ruta_scl, archivo)
                datos_bloque = core_parser_scl.parsear_bloque(ruta_completa)
                bloques_scl.append(datos_bloque)
                
            log.info(f"Extraídos datos de {len(bloques_scl)} bloques SCL.")

        # -- FASE 3: EL CEREBRO Y LOS ENLACES (LINKER) --
        registro_global = core_linker.construir_registro_global(capitulos_word, bloques_scl)
        capitulos_word, bloques_scl = core_linker.enlazar_todo(capitulos_word, bloques_scl, registro_global)

        # -- FASE 4: EL PINTOR Y LAS PLANTILLAS (RENDERER) --
        log.info("Generando archivos HTML finales...")
        
        # Pintamos el Word
        for cap in capitulos_word:
            ruta_guardado = os.path.join(ruta_destino, 'manual', cap["archivo"])
            html_renderer.renderizar_pagina(cap["titulo"], cap["contenido"], ruta_guardado)

        # Pintamos los Bloques SCL
        bloques_info_menu = []
        for bloque in bloques_scl:
            ruta_guardado = os.path.join(ruta_destino, 'bloques', f"{bloque['nombre_bloque']}.html")
            html_renderer.renderizar_bloque_scl(bloque, ruta_guardado)
            
            # Extraemos la estructura para poder dibujar el árbol lateral
            secciones = core_parser_scl.generar_secciones_menu(bloque)
            bloques_info_menu.append({"nombre": bloque['nombre_bloque'], "archivo": f"{bloque['nombre_bloque']}.html", "secciones": secciones})

        # Pintamos el Index Maestro
        log.info("Construyendo Índices de navegación...")
        manual_html = html_renderer.construir_arbol_manual(capitulos_word)
        bloques_html = html_renderer.construir_arbol_bloques(bloques_info_menu)
        pagina_inicio = f"manual/{capitulos_word[0]['archivo']}" if capitulos_word else "inicio.html"
        
        html_renderer.renderizar_index(manual_html, bloques_html, pagina_inicio, os.path.join(ruta_destino, 'index.html'))

        log.info("¡PROCESO COMPLETADO CON ÉXITO!")
        ui_dialogs.mostrar_exito(f"Ayuda corporativa generada con éxito en:\n{ruta_destino}")

    except Exception as e:
        import traceback
        log.error(f"Error crítico durante la generación:\n{traceback.format_exc()}")
        ui_dialogs.mostrar_error(f"Error crítico durante la generación. Revisa el archivo zcalm_debug.log para más detalles.\nError: {e}")

if __name__ == "__main__":
    main()