import tkinter as tk
from tkinter import filedialog, messagebox
import mammoth
import os
import re

def seleccionar_archivo_origen():
    """Abre un diálogo para seleccionar el archivo Word."""
    ruta_word = filedialog.askopenfilename(
        title="1. Selecciona el Manual en formato Word (.docx)",
        filetypes=[("Documentos de Word", "*.docx"), ("Todos los archivos", "*.*")]
    )
    return ruta_word

def seleccionar_archivo_destino():
    """Abre un diálogo para elegir dónde guardar el HTML."""
    ruta_html = filedialog.asksaveasfilename(
        title="2. Guardar página de inicio HTML como...",
        defaultextension=".html",
        initialfile="inicio.html",
        filetypes=[("Archivos HTML", "*.html")]
    )
    return ruta_html

def generar_indice_automatico(html_puro):
    """
    Busca los títulos h1, h2 y h3 y genera el HTML del menú lateral.
    Si Mammoth no generó IDs, este script se asegura de que existan.
    """
    # Buscamos todos los h1, h2 y h3
    pattern = re.compile(r'<(h[1-3])\b[^>]*>(.*?)</\1>', re.IGNORECASE | re.DOTALL)
    enlaces = []
    
    # Función para inyectar IDs si no los hay
    def add_id(match):
        tag = match.group(1)
        content = match.group(2)
        # Limpiar el texto para crear un ID válido
        clean_text = re.sub('<[^<]+?>', '', content).strip()
        id_slug = re.sub(r'[^a-z0-9]+', '_', clean_text.lower())
        enlaces.append({'tag': tag, 'id': id_slug, 'text': clean_text})
        return f'<{tag} id="{id_slug}">{content}</{tag}>'

    # Modificamos el HTML original para asegurar IDs y recolectar enlaces
    html_procesado = pattern.sub(add_id, html_puro)
    
    # Construimos el HTML del menú lateral (TOC)
    toc_html = '<div class="page-toc"><h4>Contenido</h4><ul>'
    for link in enlaces:
        indent = (int(link['tag'][1]) - 1) * 12 # Sangría según nivel h1, h2, h3
        toc_html += f'<li style="padding-left:{indent}px"><a href="#{link["id"]}">{link["text"]}</a></li>'
    toc_html += '</ul></div>'
    
    return toc_html, html_procesado

def envolver_en_plantilla(html_limpio):
    # Generamos el índice y el cuerpo procesado
    toc_sidebar, cuerpo_con_ids = generar_indice_automatico(html_limpio)
    
    plantilla = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../css/custom.css">
    <style>
        .manual-content {{ font-family: 'Segoe UI', sans-serif; color: #333; line-height: 1.6; }}
        .manual-content h1 {{ color: #005c8a; border-bottom: 3px solid #005c8a; padding-bottom: 8px; }}
        .manual-content h2 {{ color: #005c8a; border-bottom: 1px solid #ddd; padding-bottom: 5px; }}
        .manual-content table {{ width: 100%; border-collapse: collapse; margin: 20px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .manual-content td {{ border: 1px solid #dee2e6; padding: 10px; }}
        .manual-content tr:first-child td {{ background-color: #005c8a; color: white; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="page-wrapper">
        
        {toc_sidebar}

        <div class="page-content manual-content">
            {cuerpo_con_ids}
            <div style="height: 500px;"></div>
        </div>

    </div>
</body>
</html>"""
    return plantilla
    """Envuelve el código HTML extraído del Word en nuestra plantilla CSS avanzada."""
    plantilla = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../css/custom.css">
    <style>
        /* =======================================================
           ESTILOS PROFESIONALES PARA EL MANUAL (SOBRESCRIBE WORD)
           ======================================================= */
        .manual-content {{
            font-family: 'Segoe UI', Tahoma, Verdana, sans-serif;
            color: #333;
            line-height: 1.6;
        }}
        
        /* Títulos */
        .manual-content h1, .manual-content h2, .manual-content h3 {{
            color: #005c8a; /* Azul Siemens */
            margin-top: 35px;
            margin-bottom: 15px;
        }}
        .manual-content h1 {{ border-bottom: 3px solid #005c8a; padding-bottom: 8px; font-size: 28px; }}
        .manual-content h2 {{ border-bottom: 1px solid #ddd; padding-bottom: 5px; font-size: 22px; }}
        .manual-content h3 {{ font-size: 18px; color: #00334e; }}
        
        /* Párrafos */
        .manual-content p {{ margin-bottom: 15px; text-align: justify; }}
        
        /* Tablas Profesionales (Tipo Dashboard) */
        .manual-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            background-color: #fff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .manual-content td, .manual-content th {{
            border: 1px solid #dee2e6;
            padding: 12px 15px;
            vertical-align: top;
        }}
        /* Filas alternas para facilitar la lectura */
        .manual-content tr:nth-child(even) {{ background-color: #f8f9fa; }}
        
        /* TRUCO: Forzar la primera fila de CUALQUIER tabla a ser cabecera */
        .manual-content tr:first-child td, .manual-content th {{
            background-color: #005c8a;
            color: white !important;
            font-weight: bold;
        }}
        .manual-content tr:first-child td p {{ color: white !important; margin: 0; }}
        
        /* Listas limpias */
        .manual-content ul, .manual-content ol {{ margin-bottom: 20px; padding-left: 30px; }}
        .manual-content li {{ margin-bottom: 8px; }}
        
        /* Imágenes responsive (para que no rompan la pantalla si son grandes) */
        .manual-content img {{ 
            max-width: 100%; 
            height: auto; 
            border: 1px solid #ddd; 
            padding: 4px; 
            background: white; 
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin: 15px 0;
        }}
    </style>
</head>
<body>
    <div class="page-wrapper">
        <div class="page-content manual-content">
            
            {html_limpio}
            
            <div style="height: 500px;"></div>
            
        </div>
    </div>
</body>
</html>"""
    return plantilla

def main():
    # Ocultar la ventana principal de tkinter (solo queremos los pop-ups)
    root = tk.Tk()
    root.withdraw()

    print("Iniciando herramienta de conversión de Word a HTML...")

    # 1. Pedir archivo de origen
    ruta_word = seleccionar_archivo_origen()
    if not ruta_word:
        print("Operación cancelada. No se seleccionó archivo de origen.")
        return

    # 2. Pedir archivo de destino
    ruta_html = seleccionar_archivo_destino()
    if not ruta_html:
        print("Operación cancelada. No se seleccionó destino.")
        return

    print(f"Procesando: {ruta_word}")
    
    try:
        # 3. Convertir con Mammoth
        with open(ruta_word, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html_puro = result.value
            
            # Mostrar advertencias si el Word tiene formatos raros
            for message in result.messages:
                print(f"Advertencia Mammoth: {message}")

        # 4. Envolver y guardar
        html_final = envolver_en_plantilla(html_puro)
        
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write(html_final)

        print(f"¡Éxito! Archivo guardado en: {ruta_html}")
        messagebox.showinfo("Proceso completado", f"El manual se ha convertido con éxito y guardado en:\n{ruta_html}")

    except Exception as e:
        print(f"Error crítico durante la conversión: {e}")
        messagebox.showerror("Error", f"Ha ocurrido un error al procesar el documento:\n{e}")

if __name__ == "__main__":
    main()