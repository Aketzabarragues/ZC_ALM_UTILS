import logging
import json
import os

# Configuración maestra del Logger
LOG_FILE = 'zcalm_debug.log'

# Configuramos para que escriba en el archivo y también muestre por consola
logging.basicConfig(
    level=logging.DEBUG,  # Registra TODO (Debug, Info, Error)
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8'), # 'w' para que se limpie en cada nueva ejecución
        logging.StreamHandler()
    ]
)

def info(mensaje):
    """Para mensajes de progreso normales (ej: 'Procesando archivo X...')"""
    logging.info(mensaje)

def debug(mensaje):
    """Para mensajes técnicos que solo queremos ver en el .txt"""
    logging.debug(mensaje)

def error(mensaje):
    """Para registrar fallos"""
    logging.error(mensaje)

def dump_dict(nombre_diccionario, diccionario):
    """Magia pura: Convierte un diccionario de Python en texto tabulado y lo guarda en el log."""
    try:
        texto_formateado = json.dumps(diccionario, indent=4, ensure_ascii=False)
        logging.debug(f"\n{'='*50}\n[DUMP MEMORIA] -> {nombre_diccionario}\n{'-'*50}\n{texto_formateado}\n{'='*50}\n")
    except Exception as e:
        logging.error(f"No se pudo hacer dump del diccionario '{nombre_diccionario}': {e}")