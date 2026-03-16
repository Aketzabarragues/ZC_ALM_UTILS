import os
import re
import mammoth
import unicodedata

CUSTOM_CSS_CONTENT = """/* css/custom.css */
body, html { margin: 0; padding: 0; height: 100%; font-family: 'Segoe UI', Tahoma, Verdana, sans-serif; background-color: #f4f4f4; color: #333; }
body.layout-shell { overflow: hidden; }
.header { background-color: #005c8a; color: white; padding: 15px 20px; font-size: 20px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2); display: flex; justify-content: space-between; }
.main-container { display: flex; height: calc(100vh - 54px); }
.sidebar { width: 340px; background-color: #e9ecef; border-right: 1px solid #ccc; display: flex; flex-direction: column; }
.search-box { padding: 15px; background-color: #ddd; border-bottom: 1px solid #ccc; }
.search-box input { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #aaa; border-radius: 4px; }

/* MENÚ LATERAL (ÁRBOL DE NAVEGACIÓN TIPO IDE) */
.nav-list { list-style: none; padding: 10px 0; margin: 0; overflow-y: auto; flex-grow: 1; overflow-x: hidden; }
.nav-list ul { list-style: none; padding: 0; margin: 0; }
.nav-list li { margin: 0; }
.menu-item { display: flex; align-items: flex-start; padding: 6px 15px; transition: background 0.2s; cursor: pointer;}
.menu-item:hover { background-color: #dbeafe; }
.toggle-btn { width: 20px; min-width: 20px; text-align: center; color: #888; font-size: 11px; user-select: none; padding-top: 3px; }
.toggle-btn:hover { color: #005c8a; font-weight: bold; }
.toggle-spacer { width: 20px; min-width: 20px; display: inline-block; }
.menu-link { text-decoration: none; flex-grow: 1; outline: none; display: block; line-height: 1.4;}
.menu-link:hover { color: #005c8a; }
.nested { display: block; } 

/* VISOR CENTRAL Y BLOQUES */
.content-area { flex-grow: 1; background-color: white; overflow-y: auto; }
iframe { width: 100%; height: 100%; border: none; }
.page-wrapper { display: flex; max-width: 1200px; margin: 0 auto; width: 100%; }
.page-content { flex-grow: 1; padding: 30px; box-sizing: border-box; max-width: 100%; }

.doc-title { color: #005c8a; border-bottom: 2px solid #005c8a; padding-bottom: 10px; margin-bottom: 20px; }
.doc-section { background: white; margin-bottom: 20px; padding: 20px; border: 1px solid #ddd; box-shadow: 0 1px 3px rgba(0,0,0,0.05); box-sizing: border-box; width: 100%; overflow-x: auto; scroll-margin-top: 20px;}
.doc-section h3 { margin-top: 0; color: #005c8a; font-size: 18px; }

/* TABLAS RESTRINGIDAS CON SALTOS DE LÍNEA AUTOMÁTICOS */
table.doc-table { width: 100%; border-collapse: collapse; margin-top: 10px; table-layout: auto; }
table.doc-table th, table.doc-table td { border: 1px solid #ccc; padding: 10px 12px; text-align: left; vertical-align: top; line-height: 1.5; word-wrap: break-word; overflow-wrap: break-word;}
table.doc-table th { background-color: #f4f4f4; color: #005c8a; }
pre.scl-code { background-color: #f8f9fa; border-left: 4px solid #005c8a; padding: 15px; overflow-x: auto; font-family: Consolas, monospace; font-size: 13px; }

/* MANUAL WORD */
.manual-content h1 { color: #005c8a; border-bottom: 3px solid #005c8a; padding-bottom: 8px; font-size: 28px; margin-top: 35px; scroll-margin-top: 20px; }
.manual-content h2 { color: #005c8a; border-bottom: 1px solid #ddd; padding-bottom: 5px; font-size: 22px; margin-top: 30px; scroll-margin-top: 20px; }
.manual-content h3 { font-size: 18px; color: #00334e; scroll-margin-top: 20px; }
.manual-content table { width: 100%; border-collapse: collapse; margin: 25px 0; background-color: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.manual-content td, .manual-content th { border: 1px solid #dee2e6; padding: 12px 15px; }
.manual-content tr:first-child td, .manual-content th { background-color: #005c8a; color: white !important; font-weight: bold; }
.manual-content img { max-width: 100%; height: auto; border: 1px solid #ddd; padding: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin: 15px 0; }
"""

def preparar_carpetas(ruta_destino):
    carpetas = ['css', 'img', 'manual', 'bloques']
    for carpeta in carpetas:
        os.makedirs(os.path.join(ruta_destino, carpeta), exist_ok=True)
    with open(os.path.join(ruta_destino, 'css', 'custom.css'), 'w', encoding='utf-8') as f:
        f.write(CUSTOM_CSS_CONTENT)

def procesar_h3_en_contenido(html_contenido):
    """Trocea el contenido de un H1/H2 cada vez que encuentra un H3 y los envuelve en cajas blancas separadas."""
    subsecciones = []
    # Dividimos todo el texto usando las etiquetas h3 como "tijeras"
    partes_h3 = re.split(r'(<h3\b[^>]*>.*?<\/h3>)', html_contenido, flags=re.IGNORECASE | re.DOTALL)
    
    nuevo_html = ""
    
    # 1. El primer trozo es la cabecera (H1 o H2) y su párrafo introductorio. Le ponemos su propia caja blanca.
    if partes_h3[0].strip():
        nuevo_html += f'<div class="doc-section">\n{partes_h3[0]}\n</div>\n'
        
    # 2. Vamos recorriendo el resto de trozos de 2 en 2 (Etiqueta H3 + El texto que le sigue)
    for i in range(1, len(partes_h3), 2):
        h3_full = partes_h3[i]
        contenido_h3 = partes_h3[i+1] if i+1 < len(partes_h3) else ""
        
        # Leemos el título del H3 para generar su ID y pasarlo al menú izquierdo
        texto_h3 = re.sub('<[^<]+?>', '', h3_full).strip()
        texto_norm = unicodedata.normalize('NFKD', texto_h3).encode('ASCII', 'ignore').decode('utf-8')
        id_h3 = "sec_" + re.sub(r'[^a-zA-Z0-9]+', '_', texto_norm).strip('_')[:30]
        
        subsecciones.append({"id": id_h3, "titulo": texto_h3, "nivel": 3})
        
        # Metemos este H3 con su texto en UNA NUEVA CAJA BLANCA.
        # Le ponemos el id="..." a la caja entera para que el scroll te lleve directamente a la tarjeta.
        nuevo_html += f'<div class="doc-section" id="{id_h3}">\n{h3_full}\n{contenido_h3}\n</div>\n'
        
    return nuevo_html, subsecciones

def trocear_html_por_niveles(html_puro):
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
        
        # Enviamos todo el bloque (H1/H2) a procesar para que se divida en cajitas blancas
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

def resolver_enlaces_internos(capitulos):
    mapa_ids = {}
    for cap in capitulos:
        ids_encontrados = re.findall(r'\b(?:id|name)="([^"]+)"', cap["contenido"], re.IGNORECASE)
        for id_encontrado in ids_encontrados:
            mapa_ids[id_encontrado] = cap["archivo"]
            
    for cap in capitulos:
        def reemplazar_enlace(match):
            id_destino = match.group(1)
            if id_destino in mapa_ids:
                return f'href="{mapa_ids[id_destino]}#{id_destino}"'
            return match.group(0)
        cap["contenido"] = re.sub(r'href="#([^"]+)"', reemplazar_enlace, cap["contenido"], flags=re.IGNORECASE)
    return capitulos

def procesar_word(ruta_word, ruta_destino):
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
    capitulos = resolver_enlaces_internos(capitulos)
    
    for cap in capitulos:
        # Fíjate que aquí hemos quitado el <div class="doc-section"> que envolvía todo, 
        # porque la función 'procesar_h3' ya nos lo da separado en múltiples cajas.
        plantilla = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../css/custom.css">
    <style>
        /* Quitar márgenes a los títulos principales que queden primeros en su tarjeta */
        .doc-section > h1:first-child, .doc-section > h2:first-child, .doc-section > h3:first-child {{ margin-top: 0; }}
    </style>
</head>
<body>
    <div class="page-wrapper">
        <div class="page-content manual-content">
            {cap["contenido"]}
            <div style="height: 500px;"></div>
        </div>
    </div>
</body>
</html>"""
        with open(os.path.join(ruta_destino, 'manual', cap["archivo"]), "w", encoding="utf-8") as f:
            f.write(plantilla)
            
    return capitulos

def generar_index_maestro(ruta_destino, capitulos_manual, bloques_info):
    
    menu_manual = []
    for cap in capitulos_manual:
        menu_manual.append({
            "enlace": f'manual/{cap["archivo"]}',
            "titulo": cap["titulo"],
            "nivel": cap["nivel"]
        })
        for sub in cap.get("subsecciones", []):
            menu_manual.append({
                "enlace": f'manual/{cap["archivo"]}#{sub["id"]}',
                "titulo": sub["titulo"],
                "nivel": sub["nivel"]
            })

    manual_html = ""
    nivel_actual = 1
    for i, item in enumerate(menu_manual):
        nivel = item["nivel"]
        tiene_hijos = (i + 1 < len(menu_manual) and menu_manual[i+1]["nivel"] > nivel)
            
        if nivel < nivel_actual:
            for _ in range(nivel_actual - nivel): manual_html += "</ul></li>\n"
            nivel_actual = nivel
            
        pad_left = 10 + ((nivel - 1) * 22)
        
        if nivel == 1: estilo_texto = "font-weight: bold; font-size: 13.5px; color: #005c8a;"
        elif nivel == 2: estilo_texto = "font-weight: 500; font-size: 13px; color: #333;"
        else: estilo_texto = "font-weight: normal; font-size: 12.5px; color: #555; font-style: italic;"
            
        btn = '<div class="toggle-btn" onclick="toggleMenu(this)">▼</div>' if tiene_hijos else '<div class="toggle-spacer"></div>'
        manual_html += f'<li><div class="menu-item" style="padding-left: {pad_left}px;">{btn}<a class="menu-link" style="{estilo_texto}" href="{item["enlace"]}" target="visor">{item["titulo"]}</a></div>\n'
        
        if tiene_hijos:
            manual_html += '<ul class="nested" style="display: none;">\n'
            nivel_actual += 1
        else:
            manual_html += '</li>\n'
            
    for _ in range(nivel_actual - 1): manual_html += "</ul></li>\n"

    bloques_html = ""
    if bloques_info:
        for bloque in bloques_info:
            tiene_secciones = len(bloque["secciones"]) > 0
            btn_bloque = '<div class="toggle-btn" onclick="toggleMenu(this)">▼</div>' if tiene_secciones else '<div class="toggle-spacer"></div>'
            
            bloques_html += f'<li><div class="menu-item" style="padding-left: 10px;">{btn_bloque}<a class="menu-link" style="font-weight: bold; font-size: 13.5px; color: #005c8a;" href="bloques/{bloque["archivo"]}" target="visor">{bloque["nombre"]}</a></div>\n'
            
            if tiene_secciones:
                bloques_html += '<ul class="nested" style="display: none;">\n'
                nivel_actual = 2
                
                for i, sec in enumerate(bloque["secciones"]):
                    nivel = sec["nivel"]
                    tiene_hijos = (i + 1 < len(bloque["secciones"]) and bloque["secciones"][i+1]["nivel"] > nivel)
                    
                    if nivel < nivel_actual:
                        for _ in range(nivel_actual - nivel): bloques_html += "</ul></li>\n"
                        nivel_actual = nivel
                        
                    pad_left = 10 + ((nivel - 1) * 22)
                    
                    if nivel == 2: estilo_texto = "font-weight: normal; font-size: 12.5px; color: #444;"
                    else: estilo_texto = "font-weight: normal; font-size: 12px; color: #666; font-style: italic;"
                    
                    btn_sec = '<div class="toggle-btn" onclick="toggleMenu(this)">▼</div>' if tiene_hijos else '<div class="toggle-spacer"></div>'
                    bloques_html += f'<li><div class="menu-item" style="padding-left: {pad_left}px;">{btn_sec}<a class="menu-link" style="{estilo_texto}" href="bloques/{bloque["archivo"]}#{sec["id"]}" target="visor">{sec["titulo"]}</a></div>\n'
                    
                    if tiene_hijos:
                        bloques_html += '<ul class="nested" style="display: none;">\n'
                        nivel_actual += 1
                    else:
                        bloques_html += '</li>\n'
                        
                for _ in range(nivel_actual - 2): bloques_html += "</ul></li>\n"
                bloques_html += '</ul>\n'
            bloques_html += '</li>\n'
    else:
        bloques_html = '<li><div class="menu-item" style="padding-left: 10px;"><div class="toggle-spacer"></div><i class="menu-link" style="color:#999; font-size: 13px;">No hay bloques</i></div></li>'

    index_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ayuda - Zeus Control ALM</title>
    <link rel="stylesheet" href="css/custom.css">
</head>
<body class="layout-shell">
    <div class="header">
        <div>ZCALM - Documentación de Ingeniería</div>
        <div style="font-size: 14px; font-weight: normal; margin-top: 4px;">Generado automáticamente</div>
    </div>
    <div class="main-container">
        <div class="sidebar">
            <div class="search-box"><input type="text" id="buscador" placeholder="Buscar..." onkeyup="filtrarMenu()"></div>
            <ul class="nav-list" id="listaBloques">
                <li style="background-color: #e2e8f0; padding: 8px 15px; font-weight: bold; color: #334155; font-size: 11px; letter-spacing: 1px;">📚 MANUAL DEL ESTÁNDAR</li>
                {manual_html}
                <li style="background-color: #e2e8f0; padding: 8px 15px; font-weight: bold; color: #334155; font-size: 11px; letter-spacing: 1px; margin-top: 15px;">⚙️ LIBRERÍA DE BLOQUES</li>
                {bloques_html}
            </ul>
        </div>
        <div class="content-area">
            <iframe name="visor" src="manual/{capitulos_manual[0]["archivo"] if capitulos_manual else 'inicio.html'}"></iframe>
        </div>
    </div>

    <script>
        function toggleMenu(btn) {{
            var li = btn.closest('li');
            var nestedUl = Array.from(li.children).find(c => c.classList.contains('nested'));
            if (nestedUl) {{
                if (nestedUl.style.display === 'none') {{ 
                    nestedUl.style.display = 'block'; 
                    btn.innerHTML = '▼'; 
                }} else {{ 
                    nestedUl.style.display = 'none'; 
                    btn.innerHTML = '►'; 
                }}
            }}
        }}

        function filtrarMenu() {{
            var input = document.getElementById('buscador').value.toUpperCase();
            var menuItems = document.querySelectorAll('.menu-link');
            menuItems.forEach(function(a) {{
                var text = a.innerHTML.toUpperCase();
                var li = a.closest('li');
                if (text.indexOf(input) > -1) {{
                    li.style.display = "";
                    if (input !== "") {{
                        var parentUl = li.closest('ul.nested');
                        while(parentUl) {{
                            parentUl.style.display = 'block';
                            var parentLi = parentUl.closest('li');
                            if(parentLi) {{
                                parentLi.style.display = "";
                                var btn = parentLi.querySelector('.toggle-btn');
                                if(btn) btn.innerHTML = '▼';
                                parentUl = parentLi.closest('ul.nested');
                            }} else break;
                        }}
                    }}
                }} else {{
                    if (input !== "") li.style.display = "none";
                    else li.style.display = "";
                }}
            }});
        }}
        
        document.querySelectorAll('ul.nested').forEach(function(ul) {{
            var btn = ul.closest('li').querySelector('.toggle-btn');
            if(btn) btn.innerHTML = (ul.style.display === 'none') ? '►' : '▼';
        }});
    </script>
</body>
</html>"""
    with open(os.path.join(ruta_destino, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_content)