import re
import core_logger as log

def construir_registro_global(capitulos_word, bloques_scl):
    """
    PASADA 1: Crea un mapa en memoria de TODOS los identificadores del proyecto 
    y les asigna su URL definitiva.
    """
    log.info("Construyendo Registro Global de Enlaces (Cerebro)...")
    registro = {}

    # 1. Registrar todos los bloques SCL
    for bloque in bloques_scl:
        nombre = bloque["nombre_bloque"]
        # Convertimos todo a mayúsculas para evitar fallos si alguien escribe "fc2010" en lugar de "FC2010"
        registro[nombre.upper()] = {
            "tipo": "bloque_scl",
            "url": f"../bloques/{nombre}.html"
        }

    # 2. Registrar todas las anclas y títulos del Word
    for cap in capitulos_word:
        archivo_base = f"../manual/{cap['archivo']}"
        
        # A. Registrar los IDs generados por nosotros (los de los H3)
        for sub in cap.get("subsecciones", []):
            registro[sub["id"]] = {
                "tipo": "seccion_word",
                "url": f"{archivo_base}#{sub['id']}"
            }
            
        # B. Rastrear el HTML del capítulo buscando los IDs nativos invisibles que crea Word (ej. _Ref12345)
        ids_nativos = re.findall(r'\b(?:id|name)="([^"]+)"', cap["contenido"], re.IGNORECASE)
        for id_nativo in ids_nativos:
            registro[id_nativo] = {
                "tipo": "ancla_nativa_word",
                "url": f"{archivo_base}#{id_nativo}"
            }

    #log.dump_dict("REGISTRO_GLOBAL_ENLACES", registro)
    return registro


def enlazar_todo(capitulos_word, bloques_scl, registro_global):
    """
    PASADA 2: Recorre todos los datos y resuelve los hipervínculos cruzados usando el Registro.
    """
    log.info("Resolviendo dependencias e hipervínculos cruzados...")

    # --- 1. Enlazar el Word ---
    for cap in capitulos_word:
        def reemplazar_enlace_word(match):
            id_destino = match.group(1)
            # Si el enlace apunta a un ID que conocemos, reescribimos la URL
            if id_destino in registro_global:
                return f'href="{registro_global[id_destino]["url"]}"'
            # Si no (ej. un link a google.com), lo dejamos intacto
            return match.group(0)

        # Buscamos href="#algo" y lo mandamos a reemplazar
        cap["contenido"] = re.sub(r'href="#([^"]+)"', reemplazar_enlace_word, cap["contenido"], flags=re.IGNORECASE)

    # --- 2. Enlazar las dependencias de SCL ---
    enlaces_resueltos_scl = 0
    for bloque in bloques_scl:
        for dep in bloque["dependencias"]:
            if dep["tipo"] == 'normal':
                # El valor es el nombre del bloque (ej: "FC8_TRAZA_REGISTRO")
                nombre_buscado = dep["valor"].strip().upper()
                
                # Si ese nombre existe en nuestro Registro Global, le inyectamos la URL
                if nombre_buscado in registro_global:
                    dep["url"] = registro_global[nombre_buscado]["url"]
                    enlaces_resueltos_scl += 1

    log.debug(f"Se han resuelto automáticamente {enlaces_resueltos_scl} dependencias entre bloques SCL.")
    
    # Devolvemos los diccionarios ya mutados y perfectos
    return capitulos_word, bloques_scl