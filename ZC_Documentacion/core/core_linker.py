"""
Módulo Enlazador (Linker) de Referencias Cruzadas.

Este componente actúa como el motor de hipervinculación del generador.
Se encarga de construir un registro global en memoria con todos los identificadores
(Bloques SCL, UDTs, DBs y anclas del manual Word) y, posteriormente, realiza
una pasada de resolución inyectando las URLs definitivas en las dependencias
y enlaces cruzados detectados en el código.
"""

import re
from core import core_logger as log


def construir_registro_global(capitulos_word, inventario_total):
    """
    Fase 1: Escaneo y catalogación de entidades.
    
    Construye un diccionario en memoria (Hash Map) que relaciona el identificador
    único de cada entidad (nombre de bloque o ID de sección) con su URI de destino.
    
    Args:
        capitulos_word (list): Colección de capítulos procesados del manual.
        inventario_total (list): Colección combinada de bloques (FC, FB) y datos (DB, UDT).
        
    Returns:
        dict: Registro de enrutamiento global.
    """
    log.info("Construyendo Registro Global de Enrutamiento (Cerebro)...")
    registro = {}

    # 1. Indexación de bloques de código y estructuras de datos
    for bloque in inventario_total:
        nombre = bloque.get("nombre_bloque", "")
        if nombre:
            # Estandarización a mayúsculas para garantizar resolución case-insensitive
            registro[nombre.upper()] = {
                "tipo": "bloque_codigo_o_dato",
                "url": f"../bloques/{nombre}.html"
            }

    # 2. Indexación de anclas topológicas del manual (Word)
    for cap in capitulos_word:
        archivo_base = f"../manual/{cap.get('archivo', '')}"
        
        # A. Indexar secciones explícitas (H3) generadas por nuestro parser
        for sub in cap.get("subsecciones", []):
            id_sub = sub.get("id")
            if id_sub:
                registro[id_sub] = {
                    "tipo": "seccion_word",
                    "url": f"{archivo_base}#{id_sub}"
                }
            
        # B. Indexar marcadores nativos de anclaje de Microsoft Word (_Ref...)
        contenido_cap = cap.get("contenido", "")
        ids_nativos = re.findall(r'\b(?:id|name)="([^"]+)"', contenido_cap, re.IGNORECASE)
        for id_nativo in ids_nativos:
            registro[id_nativo] = {
                "tipo": "ancla_nativa_word",
                "url": f"{archivo_base}#{id_nativo}"
            }

    return registro


def enlazar_todo(capitulos_word, inventario_total, registro_global):
    """
    Fase 2: Resolución estática de dependencias cruzadas.
    
    Recorre los documentos y bloques parseados, detectando referencias a otras entidades
    y sobrescribiendo sus atributos/enlaces con las URLs consolidadas del registro global.
    
    Args:
        capitulos_word (list): Colección de capítulos del manual.
        inventario_total (list): Inventario completo de bloques SCL y datos.
        registro_global (dict): Mapa de rutas generado en la Fase 1.
        
    Returns:
        tuple: (capitulos_word, inventario_total) con las URIs ya inyectadas.
    """
    log.info("Resolviendo matriz de dependencias e hipervínculos cruzados...")

    # --- 1. Resolución de referencias internas del Manual (Word) ---
    for cap in capitulos_word:
        def reemplazar_enlace_word(match):
            id_destino = match.group(1)
            # Inyección de URL si el ancla destino existe en nuestro ecosistema
            if id_destino in registro_global:
                return f'href="{registro_global[id_destino]["url"]}"'
            # Preservación del enlace original si es externo (ej. protocolo HTTP)
            return match.group(0)

        # Intercepción de atributos href basados en anclas (#)
        if "contenido" in cap:
            cap["contenido"] = re.sub(
                r'href="#([^"]+)"', 
                reemplazar_enlace_word, 
                cap["contenido"], 
                flags=re.IGNORECASE
            )

    # --- 2. Resolución de dependencias (Requires) en bloques de código ---
    enlaces_resueltos_scl = 0
    for bloque in inventario_total:
        
        # PREVENCIÓN DE ERROR: Uso de .get() seguro en caso de que la entidad (ej. un UDT) 
        # no posea la clave 'dependencias' en su estructura de datos original.
        dependencias = bloque.get("dependencias", [])
        
        for dep in dependencias:
            if dep.get("tipo") == 'normal' and "valor" in dep:
                # El valor declarado en el tag Requires (Ej: "FC8_TRAZA_REGISTRO")
                nombre_buscado = dep["valor"].strip().upper()
                
                # Inyección de hipervínculo si el componente es un ciudadano de nuestro registro
                if nombre_buscado in registro_global:
                    dep["url"] = registro_global[nombre_buscado]["url"]
                    enlaces_resueltos_scl += 1

    log.debug(f"Resolución finalizada: {enlaces_resueltos_scl} dependencias cruzadas inyectadas en el código fuente.")
    
    return capitulos_word, inventario_total