import os
import re
import mammoth
import unicodedata
import core_logger as log

def procesar_h3_en_contenido(html_contenido):
    """Detecta los H3, crea sus identificadores únicos y prepara las subsecciones."""
    subsecciones = []
    partes_h3 = re.split(r'(<h3\b[^>]*>.*?<\/h3>)', html_contenido, flags=re.IGNORECASE | re.DOTALL)
    nuevo_html = ""
    
    if partes_h3[0].strip():
        nuevo_html += f'<div class="doc-section">\n{partes_h3[0]}\n</div>\n'
        
    for i in range(1, len(partes_h3), 2):
        h3_full = partes_h3[i]
        contenido_h3 = partes_h3[i+1] if i+1 < len(partes_h3) else ""
        
        texto_h3 = re.sub('<[^<]+?>', '', h3_full).strip()
        texto_norm = unicodedata.normalize('NFKD', texto_h3).encode('ASCII', 'ignore').decode('utf-8')
        id_h3 = "sec_" + re.sub(r'[^a-zA-Z0-9]+', '_', texto_norm).strip('_')[:30]
        
        subsecciones.append({"id": id_h3, "titulo": texto_h3, "nivel": 3})
        nuevo_html += f'<div class="doc-section" id="{id_h3}">\n{h3_full}\n{contenido_h3}\n</div>\n'
        
    return nuevo_html, subsecciones

def trocear_html_por_niveles(html_puro):
    """Trocea el documento gigante en capítulos (H1/H2)."""
    partes = re.split(r'(<(h[12])\b[^>]*>.*?<\/\2>)', html_puro, flags=re.IGNORECASE | re.DOTALL)
    capitulos = []
    
    if partes[0].strip():
        html_mod, subsecciones = procesar_h3_en_contenido(partes[0])
        capitulos.append({"archivo": "000_portada.html", "titulo": "Portada y Revisiones", "nivel": 1, "contenido": html_mod, "subsecciones": subsecciones})
    
    contador = 1
    for i in range(1, len(partes), 3):
        etiqueta_completa = partes[i]
        tipo_header = partes[i+1].lower() 
        contenido_subsecuente = partes[i+2] if i+2 < len(partes) else ""
        
        texto_limpio = re.sub('<[^<]+?>', '', etiqueta_completa).strip()
        texto_normalizado = unicodedata.normalize('NFKD', texto_limpio).encode('ASCII', 'ignore').decode('utf-8')
        nombre_seguro = re.sub(r'[^a-zA-Z0-9]+', '_', texto_normalizado).strip('_')[:50]
        
        contenido_total = etiqueta_completa + contenido_subsecuente
        html_mod, subsecciones = procesar_h3_en_contenido(contenido_total)
        
        capitulos.append({
            "archivo": f"{contador:03d}_{nombre_seguro}.html",
            "titulo": texto_limpio,
            "nivel": int(tipo_header[1]),
            "contenido": html_mod,
            "subsecciones": subsecciones
        })
        contador += 1
    return capitulos

def procesar_word(ruta_word, ruta_destino):
    """Extrae el Word, guarda las imágenes en el destino y devuelve la lista de datos."""
    log.info("Iniciando extracción del documento Word...")
    ruta_img = os.path.join(ruta_destino, 'img')
    contador_img = 1

    def convertir_imagen(image):
        nonlocal contador_img
        extension = image.content_type.split("/")[1]
        nombre_img = f"img_{contador_img}.{extension}"
        with image.open() as image_stream:
            with open(os.path.join(ruta_img, nombre_img), "wb") as f:
                f.write(image_stream.read())
        contador_img += 1
        return {"src": f"../img/{nombre_img}"}

    with open(ruta_word, "rb") as docx_file:
        resultado = mammoth.convert_to_html(docx_file, convert_image=mammoth.images.img_element(convertir_imagen))
    
    capitulos = trocear_html_por_niveles(resultado.value)
    
    # Volcamos a log para debug (imprimimos solo los metadatos para no saturar el log con todo el HTML gigante)
    resumen_log = [{"archivo": c["archivo"], "titulo": c["titulo"], "subs": [s["titulo"] for s in c["subsecciones"]]} for c in capitulos]
    #log.dump_dict("ESTRUCTURA_WORD_EXTRAIDA", resumen_log)
    
    return capitulos