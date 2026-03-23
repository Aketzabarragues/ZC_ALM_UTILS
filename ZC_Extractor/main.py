import argparse
import os
import extractor_procesos
import extractor_preal
import extractor_pint
import extractor_alarmas
import extractor_etapas
import extractor_disp_ed
import extractor_disp_ea
import extractor_disp_sa
import extractor_disp_v
import extractor_disp_m
import extractor_disp_m_vf
import extractor_config_disp

def ejecutar_todo(ruta_excel):

    # 1. Definimos la carpeta base
    base_temp = os.path.join(os.environ['TEMP'], "_ZC_ALM_TOOLS")
    # Python genera datos para que C# los lea, así que los guardaremos en 'Temp' 
    # para dejar 'Export' solo para lo que sale de TIA Portal.
    folder_path = os.path.join(base_temp, "Export")
    os.makedirs(folder_path, exist_ok=True)
    
    # Lista de funciones a ejecutar
    operaciones = [
        ("Procesos", extractor_procesos.extraer),
        ("PReal", extractor_preal.extraer),
        ("PInt", extractor_pint.extraer),
        ("Alarmas", extractor_alarmas.extraer),
        ("Etapas", extractor_etapas.extraer),
        ("Disp_ED", extractor_disp_ed.extraer),
        ("Disp_EA", extractor_disp_ea.extraer),
        ("Disp_SA", extractor_disp_sa.extraer),        
        ("Disp_V", extractor_disp_v.extraer),
        ("Disp_M", extractor_disp_m.extraer),
        ("Disp_M_VF", extractor_disp_m_vf.extraer),
        ("Disp_Config", extractor_config_disp.extraer)
    ]
    
    resultados_globales = []

    for nombre, funcion_extraer in operaciones:
        print(f"Iniciando extracción de: {nombre}...")
        # Pasamos la carpeta de destino a la función
        exito, mensaje = funcion_extraer(ruta_excel, folder_path)
        
        if exito:
            resultados_globales.append(f"OK: {nombre}")
        else:
            resultados_globales.append(f"ERROR en {nombre}: {mensaje}")
            
    return resultados_globales

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="Ruta al archivo Excel")
    args = parser.parse_args()

    if os.path.exists(args.path):
        status = ejecutar_todo(args.path)
        print("\n".join(status))
        print("DONE")
    else:
        print(f"ERROR: No se encuentra el archivo en {args.path}")