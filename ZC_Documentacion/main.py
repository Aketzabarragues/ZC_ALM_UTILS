"""
Módulo Principal del Generador de Documentación de Zeus Control.

Este script actúa como el controlador central de la aplicación. Gestiona el flujo 
de ejecución completo: carga de configuración, orquestación de los distintos 
analizadores (parsers de Word y SCL/Datos), resolución de dependencias cruzadas 
(Linker) y generación final de las vistas estáticas en formato HTML.
"""

import os
import re
import sys
import json
import traceback

# Módulos internos del core de ZCALM
from core import core_logger as log
from core import core_parser_word
from core import core_parser_scl
from core import core_parser_data
from core import core_linker
from ui import html_renderer

# Archivo local de persistencia para las rutas de trabajo del usuario
CONFIG_FILE = "config.json"


def cargar_configuracion():
    """
    Lee el archivo de configuración en formato JSON.
    
    Si el archivo no existe o su formato es inválido, retorna un diccionario 
    con las claves por defecto vacías para evitar excepciones en tiempo de 
    ejecución y forzar al usuario a definirlas mediante la interfaz.
    
    Returns:
        dict: Diccionario con las rutas de configuración.
    """
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
        log.error(f"Error de lectura en {CONFIG_FILE}: {e}")
        return config_por_defecto


def guardar_configuracion(config):
    """
    Serializa y persiste el diccionario de configuración en disco.
    """
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        log.error(f"Error de escritura en {CONFIG_FILE}: {e}")


def modificar_configuracion():
    """
    Interfaz interactiva por consola para la actualización de rutas de trabajo.
    Permite arrastrar y soltar carpetas directamente sobre la terminal.
    """
    print("\n--- MODIFICAR CONFIGURACIÓN ---")
    print("Consejo: Arrastra la carpeta/archivo a esta ventana o pega la ruta.")
    print("Pulsa ENTER sin escribir nada para mantener la ruta actual.\n")
    
    config = cargar_configuracion()

    print(f"Actual: {config['ruta_word']}")
    nueva_word = input("Nueva ruta del documento Word (.docx): ").strip('\"\' ')
    if nueva_word: 
        config['ruta_word'] = nueva_word

    print(f"\nActual: {config['ruta_fuentes']}")
    nueva_fuentes = input("Nueva ruta de la carpeta de fuentes (SCL/DB/UDT): ").strip('\"\' ')
    if nueva_fuentes: 
        config['ruta_fuentes'] = nueva_fuentes

    print(f"\nActual: {config['ruta_destino']}")
    nuevo_destino = input("Nueva ruta del directorio de SALIDA (HTML): ").strip('\"\' ')
    if nuevo_destino: 
        config['ruta_destino'] = nuevo_destino

    guardar_configuracion(config)
    print("\n[OK] Configuración actualizada correctamente.")


def generar_documentacion():
    """
    Ejecuta el pipeline principal de extracción y generación de documentación.
    
    Fases del proceso:
    1. Extracción y parseo de datos del manual (Word).
    2. Escaneo y parseo de código fuente SCL y estructuras de datos (DB/UDT).
    3. Vinculación (Linking) para resolución de referencias cruzadas.
    4. Renderización de plantillas Jinja2 a HTML estático.
    5. Estructuración y ordenación del árbol de navegación lateral.
    """
    config = cargar_configuracion()
    
    ruta_word = config.get("ruta_word")
    ruta_scl = config.get("ruta_fuentes")
    ruta_destino = config.get("ruta_destino")

    # Validación pre-ejecución de rutas críticas
    if not ruta_word or not os.path.exists(ruta_word):
        print("\n[ERROR] La ruta del archivo Word especificada no es válida.")
        return
    if not ruta_destino:
        print("\n[ERROR] El directorio de destino no está configurado.")
        return

    print("\n" + "="*49)
    print(" ZCALM - GENERADOR DE DOCUMENTACIÓN TÉCNICA v3.0 ")
    print("="*49)

    try:
        log.info(f"Inicializando despliegue estático en: {ruta_destino}")
        html_renderer.copiar_estaticos(ruta_destino)

        # FASE 1: Procesamiento del documento funcional (Manual)
        capitulos_word = core_parser_word.procesar_word(ruta_word, ruta_destino)

        # FASE 2: Extracción de lógica y datos desde exportaciones VCI
        bloques_scl = []
        bloques_datos = []
        
        if ruta_scl and os.path.exists(ruta_scl):
            log.info(f"Iniciando escaneo de código fuente en: {ruta_scl}")
            archivos_fuente = [f for f in os.listdir(ruta_scl) if f.lower().endswith(('.scl', '.db', '.udt'))]
            
            for archivo in archivos_fuente:
                ruta_completa = os.path.join(ruta_scl, archivo)
                
                # Desvío según el formato del archivo fuente
                if archivo.lower().endswith('.scl'):
                    datos_bloque = core_parser_scl.parsear_bloque(ruta_completa)
                    if datos_bloque: 
                        bloques_scl.append(datos_bloque)
                
                elif archivo.lower().endswith(('.db', '.udt')):
                    datos_extraidos = core_parser_data.parsear_archivo_datos(ruta_completa)
                    bloques_datos.extend(datos_extraidos)
                    
            log.info(f"Parseo finalizado: {len(bloques_scl)} bloques SCL, {len(bloques_datos)} estructuras DB/UDT.")

        # FASE 3: Enlazador (Linker) - Generación del árbol de dependencias
        # Agrupamos todo (SCL + DB/UDT) para que el registro global conozca todos los archivos
        inventario_total = bloques_scl + bloques_datos        
        registro_global = core_linker.construir_registro_global(capitulos_word, inventario_total)        
        # Procesamos los enlaces para todo el inventario completo
        capitulos_word, inventario_total = core_linker.enlazar_todo(capitulos_word, inventario_total, registro_global)

        # FASE 4: Renderizado de Vistas (HTML)
        log.info("Iniciando compilación de vistas HTML...")
        
        # Renderizado del Manual
        for cap in capitulos_word:
            ruta_guardado = os.path.join(ruta_destino, 'manual', cap["archivo"])
            html_renderer.renderizar_pagina(cap["titulo"], cap["contenido"], ruta_guardado)

        bloques_info_menu = []

        # Renderizado de Funciones y FBs
        for bloque in bloques_scl:
            ruta_guardado = os.path.join(ruta_destino, 'bloques', f"{bloque['nombre_bloque']}.html")
            html_renderer.renderizar_bloque_scl(bloque, ruta_guardado)
            
            secciones = core_parser_scl.generar_secciones_menu(bloque)
            
            # Clasificación heurística del tipo de bloque basándose en el prefijo estándar
            nombre_upper = bloque['nombre_bloque'].upper()
            if nombre_upper.startswith('FC'):
                tipo_bloque = 'FC'
            elif nombre_upper.startswith('FB'):
                tipo_bloque = 'FB'
            elif nombre_upper.startswith('DB'):
                tipo_bloque = 'DB'
            else:
                tipo_bloque = 'UDT'
            
            bloques_info_menu.append({
                "nombre": bloque['nombre_bloque'], 
                "archivo": f"{bloque['nombre_bloque']}.html", 
                "secciones": secciones,
                "tipo": tipo_bloque
            })

        # Renderizado de Tipos de Datos y Data Blocks
        for bloque_dato in bloques_datos:
            ruta_guardado = os.path.join(ruta_destino, 'bloques', f"{bloque_dato['nombre_bloque']}.html")
            html_renderer.renderizar_datos(bloque_dato, ruta_guardado)
            
            # Clasificación binaria estricta para el menú de datos
            tipo_dato = 'DB' if bloque_dato['nombre_bloque'].upper().startswith('DB') else 'UDT'
            
            bloques_info_menu.append({
                "nombre": bloque_dato['nombre_bloque'], 
                "archivo": f"{bloque_dato['nombre_bloque']}.html", 
                "secciones": [], 
                "tipo": tipo_dato
            })

        # FASE 5: Construcción y ordenación del Índice Lateral
        def orden_natural_por_numero(item):
            """
            Algoritmo de ordenación natural focalizado en la numeración Siemens.
            
            Extrae el primer identificador numérico encontrado en el nombre del bloque
            para realizar una ordenación matemática estricta (ej. FC8 precederá a FB2010),
            ignorando el tipo de bloque. Si no posee identificador, se delega al final.
            """
            texto = item["nombre"]
            match = re.search(r'\d+', texto)
            numero = int(match.group()) if match else 9999999
            
            # Retorna tupla para desempatar alfabéticamente si comparten número (o carecen de él)
            return (numero, texto.upper())
            
        bloques_info_menu.sort(key=orden_natural_por_numero)

        # Segmentación del inventario para su distribución en el layout principal
        funciones_info = [b for b in bloques_info_menu if b['tipo'] in ['FC', 'FB']]
        datos_info     = [b for b in bloques_info_menu if b['tipo'] in ['DB', 'UDT']]

        log.info("Ensamblando dom del índice de navegación...")
        manual_html = html_renderer.construir_arbol_manual(capitulos_word)
        funciones_html = html_renderer.construir_arbol_bloques(funciones_info)
        datos_html = html_renderer.construir_arbol_bloques(datos_info)
        
        # Enrutamiento de la vista por defecto al abrir la aplicación
        pagina_inicio = f"manual/{capitulos_word[0]['archivo']}" if capitulos_word else "inicio.html"
        
        # Renderizado del contenedor primario (Index)
        html_renderer.renderizar_index(
            manual_html, 
            funciones_html, 
            datos_html, 
            pagina_inicio, 
            os.path.join(ruta_destino, 'index.html')
        )

        log.info("Proceso de generación finalizado con éxito.")

    except Exception as e:
        # Captura de errores fatales no previstos durante el pipeline
        log.error(f"Fallo estructural durante la ejecución:\n{traceback.format_exc()}")


def mostrar_menu():
    """
    Bucle principal de la interfaz CLI de la aplicación.
    Mantiene la ejecución activa hasta que el usuario decida salir.
    """
    while True:
        print("\n" + "="*40)
        print(" ZCALM - INTERFAZ DE ADMINISTRACIÓN")
        print("="*40)
        print("1. Iniciar compilación de documentación")
        print("2. Configurar entornos de trabajo (Rutas)")
        print("3. Finalizar sesión")
        print("="*40)
        
        opcion = input("Seleccione una operación (1-3): ").strip()
        
        if opcion == '1':
            generar_documentacion()
        elif opcion == '2':
            modificar_configuracion()
        elif opcion == '3':
            print("Cerrando herramientas ZCALM...")
            sys.exit(0)
        else:
            print("[!] Operación no reconocida. Valores válidos: 1, 2 o 3.")


if __name__ == "__main__":
    # Punto de entrada de la aplicación
    mostrar_menu()