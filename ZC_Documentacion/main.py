import os
import sys
import json
import core_logger as log
import core_parser_word
import core_parser_scl
import core_parser_data
import core_linker
import html_renderer

# Nombre del archivo de configuración
CONFIG_FILE = "zcalm_config.json"

def cargar_configuracion():
    """Carga el archivo JSON. Si no existe, lo crea con valores vacíos."""
    config_por_defecto = {
        "ruta_word": "",
        "ruta_fuentes": "",
        "ruta_destino": ""
    }
    
    if not os.path.exists(CONFIG_FILE):
        guardar_configuracion(config_por_defecto)
        return config_por_defecto

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log.error(f"Error leyendo {CONFIG_FILE}: {e}")
        return config_por_defecto

def guardar_configuracion(config):
    """Guarda el diccionario de configuración en el archivo JSON."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        log.error(f"Error guardando {CONFIG_FILE}: {e}")

def modificar_configuracion():
    """Menú interactivo para cambiar las rutas."""
    print("\n--- MODIFICAR CONFIGURACIÓN ---")
    print("Consejo: Arrastra la carpeta/archivo a esta ventana o pega la ruta.")
    print("Pulsa ENTER sin escribir nada para mantener la ruta actual.\n")
    
    config = cargar_configuracion()

    # 1. Ruta Word
    print(f"Actual: {config['ruta_word']}")
    nueva_word = input("Nueva ruta del documento Word (.docx): ").strip('\"\' ')
    if nueva_word: config['ruta_word'] = nueva_word

    # 2. Ruta Fuentes (SCL/DB/UDT)
    print(f"\nActual: {config['ruta_fuentes']}")
    nueva_fuentes = input("Nueva ruta de la carpeta de fuentes exportadas: ").strip('\"\' ')
    if nueva_fuentes: config['ruta_fuentes'] = nueva_fuentes

    # 3. Ruta Destino
    print(f"\nActual: {config['ruta_destino']}")
    nuevo_destino = input("Nueva ruta de la carpeta de SALIDA (HTML): ").strip('\"\' ')
    if nuevo_destino: config['ruta_destino'] = nuevo_destino

    guardar_configuracion(config)
    print("\n[OK] Configuración guardada correctamente.")

def generar_documentacion():
    """Ejecuta el proceso core de generación leyendo el JSON."""
    config = cargar_configuracion()
    
    ruta_word = config.get("ruta_word")
    ruta_scl = config.get("ruta_fuentes")
    ruta_destino = config.get("ruta_destino")

    # Validaciones básicas
    if not ruta_word or not os.path.exists(ruta_word):
        print("\n[ERROR] La ruta del archivo Word no es válida. Ve a la opción 2.")
        return
    if not ruta_destino:
        print("\n[ERROR] La ruta de destino no está configurada. Ve a la opción 2.")
        return

    print("\n=================================================")
    print(" ZCALM - GENERADOR DE DOCUMENTACIÓN v3.0 (PRO)   ")
    print("=================================================")

    try:
        log.info(f"Iniciando proceso en la ruta destino: {ruta_destino}")
        html_renderer.copiar_estaticos(ruta_destino)

        # -- FASE 1 y 2: EXTRAER DATOS (WORD) --
        capitulos_word = core_parser_word.procesar_word(ruta_word, ruta_destino)

        # -- FASE 1 y 2: EXTRAER DATOS (SCL, DB y UDT) --
        bloques_scl = []
        bloques_datos = []
        
        if ruta_scl and os.path.exists(ruta_scl):
            log.info(f"Escaneando carpeta fuentes: {ruta_scl}")
            archivos_fuente = [f for f in os.listdir(ruta_scl) if f.lower().endswith(('.scl', '.db', '.udt'))]
            
            for archivo in archivos_fuente:
                ruta_completa = os.path.join(ruta_scl, archivo)
                
                if archivo.lower().endswith('.scl'):
                    datos_bloque = core_parser_scl.parsear_bloque(ruta_completa)
                    if datos_bloque: bloques_scl.append(datos_bloque)
                
                elif archivo.lower().endswith(('.db', '.udt')):
                    datos_extraidos = core_parser_data.parsear_archivo_datos(ruta_completa)
                    bloques_datos.extend(datos_extraidos)
                    
            log.info(f"Extraídos {len(bloques_scl)} bloques SCL y {len(bloques_datos)} estructuras de datos (DB/UDT).")

        # -- FASE 3: EL CEREBRO Y LOS ENLACES (LINKER) --
        registro_global = core_linker.construir_registro_global(capitulos_word, bloques_scl)
        capitulos_word, bloques_scl = core_linker.enlazar_todo(capitulos_word, bloques_scl, registro_global)

        # -- FASE 4: EL PINTOR Y LAS PLANTILLAS (RENDERER) --
        log.info("Generando archivos HTML finales...")
        
        for cap in capitulos_word:
            ruta_guardado = os.path.join(ruta_destino, 'manual', cap["archivo"])
            html_renderer.renderizar_pagina(cap["titulo"], cap["contenido"], ruta_guardado)

        bloques_info_menu = []
        
        # SCL
        for bloque in bloques_scl:
            ruta_guardado = os.path.join(ruta_destino, 'bloques', f"{bloque['nombre_bloque']}.html")
            html_renderer.renderizar_bloque_scl(bloque, ruta_guardado)
            secciones = core_parser_scl.generar_secciones_menu(bloque)
            bloques_info_menu.append({
                "nombre": bloque['nombre_bloque'], "archivo": f"{bloque['nombre_bloque']}.html", 
                "secciones": secciones, "tipo": "SCL"
            })

        # Datos (UDT/DB)
        for bloque_dato in bloques_datos:
            ruta_guardado = os.path.join(ruta_destino, 'bloques', f"{bloque_dato['nombre_bloque']}.html")
            html_renderer.renderizar_datos(bloque_dato, ruta_guardado)
            bloques_info_menu.append({
                "nombre": bloque_dato['nombre_bloque'], "archivo": f"{bloque_dato['nombre_bloque']}.html", 
                "secciones": [], "tipo": bloque_dato['tipo']
            })

        log.info("Construyendo Índices de navegación...")
        manual_html = html_renderer.construir_arbol_manual(capitulos_word)
        bloques_html = html_renderer.construir_arbol_bloques(bloques_info_menu)
        pagina_inicio = f"manual/{capitulos_word[0]['archivo']}" if capitulos_word else "inicio.html"
        
        html_renderer.renderizar_index(manual_html, bloques_html, pagina_inicio, os.path.join(ruta_destino, 'index.html'))

        print("\n[ÉXITO] ¡Proceso completado! Documentación generada en:")
        print(f"-> {ruta_destino}")

    except Exception as e:
        import traceback
        print("\n[ERROR CRÍTICO] Ha ocurrido un fallo durante la generación.")
        print(f"Detalle: {e}")
        log.error(f"Error crítico durante la generación:\n{traceback.format_exc()}")

def mostrar_menu():
    """Bucle principal de la aplicación de consola."""
    while True:
        print("\n" + "="*40)
        print(" ZCALM - HERRAMIENTA DE DOCUMENTACIÓN")
        print("="*40)
        print("1. Generar documentación")
        print("2. Modificar configuración (rutas)")
        print("3. Salir")
        print("="*40)
        
        opcion = input("Elige una opción (1-3): ").strip()
        
        if opcion == '1':
            generar_documentacion()
        elif opcion == '2':
            modificar_configuracion()
        elif opcion == '3':
            print("Saliendo de la aplicación...")
            sys.exit(0)
        else:
            print("[!] Opción no válida. Por favor, introduce 1, 2 o 3.")

if __name__ == "__main__":
    mostrar_menu()