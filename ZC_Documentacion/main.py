import ui_dialogs
import doc_builder
import scl_parser
import os
from tkinter import filedialog

def seleccionar_carpeta_scl():
    return filedialog.askdirectory(title="3. (Opcional) Selecciona la carpeta con los fuentes SCL exportados")

def main():
    ui_dialogs.inicializar_ui()
    
    print("===========================================")
    print(" ZCALM - GENERADOR DE DOCUMENTACIÓN v1.4   ")
    print("===========================================")

    ruta_word = ui_dialogs.seleccionar_archivo_origen()
    if not ruta_word: return
    ruta_scl = seleccionar_carpeta_scl()
    ruta_destino = ui_dialogs.seleccionar_carpeta_destino()
    if not ruta_destino: return

    try:
        print(f"\n1. Creando estructura de carpetas en: {ruta_destino}")
        doc_builder.preparar_carpetas(ruta_destino)

        print(f"2. Extrayendo manual y separando imágenes...")
        capitulos = doc_builder.procesar_word(ruta_word, ruta_destino)
        
        bloques_info = []

        if ruta_scl and os.path.exists(ruta_scl):
            print(f"3. Parseando bloques SCL desde: {ruta_scl}")
            archivos_scl = [f for f in os.listdir(ruta_scl) if f.lower().endswith('.scl')]
            
            for archivo in archivos_scl:
                ruta_completa = os.path.join(ruta_scl, archivo)
                # AQUÍ EL CAMBIO: Recogemos 5 variables (añadido contenido_original)
                nombre, etiquetas, variables, regiones, contenido_original = scl_parser.parsear_scl(ruta_completa)
                
                # Le pasamos el contenido_original al generador HTML
                secciones = scl_parser.generar_html_bloque(nombre, etiquetas, variables, regiones, contenido_original, ruta_destino)
                
                bloques_info.append({
                    "nombre": nombre,
                    "archivo": f"{nombre}.html",
                    "secciones": secciones
                })
            print(f"   -> ¡{len(archivos_scl)} bloques documentados con éxito!")
        
        print(f"4. Generando Index de Navegación Maestro...")
        doc_builder.generar_index_maestro(ruta_destino, capitulos, bloques_info)

        ui_dialogs.mostrar_exito(f"Ayuda generada correctamente en:\n{ruta_destino}\n\nAbre el archivo 'index.html'.")

    except Exception as e:
        import traceback
        traceback.print_exc()
        ui_dialogs.mostrar_error(f"Error durante el procesamiento:\n{e}")

if __name__ == "__main__":
    main()