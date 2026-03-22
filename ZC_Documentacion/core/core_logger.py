"""
Sistema Centralizado de Telemetría y Registro (Logger).

Este módulo proporciona un wrapper sobre la librería estándar 'logging' de Python.
Está diseñado para ofrecer un flujo de salida dual: una salida estándar (consola) 
para la interacción con el usuario y una salida persistente (archivo) para 
el rastreo de bajo nivel y la depuración de estructuras de datos complejas.
"""

import logging
import json
import os

# Archivo local de salida para la persistencia de las trazas de ejecución
LOG_FILE = 'debug.log'

# ==============================================================================
# CONFIGURACIÓN DEL MOTOR DE LOGS
# ==============================================================================
# Se utiliza el modo 'w' (write) en el FileHandler para asegurar que el archivo 
# de log se sobreescriba y pertenezca exclusivamente a la última ejecución, 
# evitando archivos residuales gigantescos (stateless logging).
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


def info(mensaje):
    """
    Registra un evento de telemetría de nivel informativo.
    
    Utilizado para indicar el progreso del pipeline principal (ej. inicio de 
    fases, conteo de archivos procesados, operaciones I/O exitosas).
    
    Args:
        mensaje (str): Cadena de texto a registrar.
    """
    logging.info(mensaje)


def debug(mensaje):
    """
    Registra un evento de telemetría de bajo nivel (diagnóstico).
    
    Utilizado para trazas técnicas que son ruidosas para el usuario final en 
    consola, pero críticas para el análisis post-mortem en el archivo de log.
    
    Args:
        mensaje (str): Cadena de texto técnica a registrar.
    """
    logging.debug(mensaje)


def error(mensaje):
    """
    Registra un evento de fallo o excepción crítica en el sistema.
    
    Activa la salida de error estándar y preserva el contexto del fallo 
    para facilitar su posterior resolución.
    
    Args:
        mensaje (str): Descripción del error o traza de la excepción.
    """
    logging.error(mensaje)


def dump_dict(nombre_diccionario, diccionario):
    """
    Serializa y vuelca el estado de un objeto en memoria al archivo de log.
    
    Convierte diccionarios y listas complejas (como el Registro Global o los objetos 
    parseados del SCL) en cadenas JSON formateadas e indentadas. Es una herramienta 
    puramente analítica para validar los Contratos de Datos (DTOs).
    
    Args:
        nombre_diccionario (str): Etiqueta identificativa para localizar el volcado.
        diccionario (dict|list): Objeto o estructura de datos a inspeccionar.
    """
    try:
        # ensure_ascii=False garantiza la correcta representación de tildes (UTF-8)
        texto_formateado = json.dumps(diccionario, indent=4, ensure_ascii=False)
        
        # Volcado estructurado visualmente para facilitar la lectura en el archivo plano
        logging.debug(
            f"\n{'='*60}\n"
            f"[DUMP MEMORIA] -> {nombre_diccionario}\n"
            f"{'-'*60}\n"
            f"{texto_formateado}\n"
            f"{'='*60}\n"
        )
    except Exception as e:
        logging.error(f"Fallo durante la serialización del objeto '{nombre_diccionario}': {str(e)}")