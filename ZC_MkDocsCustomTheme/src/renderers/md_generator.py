from pathlib import Path
from domain.models import SiemensBlock

def generar_markdown_bloque(bloque: SiemensBlock, output_dir: Path) -> Path:
    md_lines = [f"# {bloque.name} ({bloque.block_type.value})", ""]

    # Función auxiliar para crear tarjetas aisladas garantizando la indentación de Markdown
    def add_card(title: str, icon: str, content_lines: list):
        md_lines.extend([
            '<div class="grid cards" markdown>',
            '',
            f'-   :{icon}: __{title}__',
            '',
            '    ---'
        ])
        # Todo el contenido de la tarjeta DEBE ir indentado 4 espacios para pertenecer al elemento de lista '-'
        for line in content_lines:
            md_lines.append(f'    {line}' if line.strip() else '')
        md_lines.extend(['', '</div>', ''])

    # 1. Información del Sistema
    info_lines = [
        f'**Versión:** {bloque.version or "-"}<br>',
        f'**Autor:** {bloque.author or "-"}<br>',
        f'**Familia:** {bloque.family or "-"}<br>',
        f'**Hardware:** {bloque.system_info.hardware or "-"}<br>',
        f'**Ingeniería:** {bloque.system_info.engineering or "-"}'
    ]
    add_card("Información del Sistema", "material-information-outline", info_lines)

    # 2. Restricciones
    if bloque.restrictions and bloque.restrictions.lower() != "ninguna.":
        add_card("Restricciones", "material-alert-outline", [bloque.restrictions])
    else:
        add_card("Restricciones", "material-check-circle-outline", ["Ninguna limitación operativa."])

    # 3. Descripción Funcional
    if bloque.description:
        add_card("Descripción Funcional", "material-text-box-outline", bloque.description.splitlines())

    # 4. Dependencias Requeridas
    if bloque.dependencies:
        dep_lines = []
        for dep in bloque.dependencies:
            elements_clean = [e.strip().replace('`', '') for e in dep.elements.split(',')]
            links = []
            for e in elements_clean:
                if e == "-": continue
                folder = "Bloques de codigo" if e.startswith("FC") or e.startswith("FB") else "Estructura de datos"
                links.append(f"[{e}](../{folder}/{e}.md)")
            if links:
                dep_lines.append(f'**{dep.type}:** {", ".join(links)}<br>')
        if dep_lines:
            add_card("Dependencias Requeridas", "material-puzzle-outline", dep_lines)

    # 5. Historial de Cambios
    if bloque.changelog_md:
        add_card("Historial de Cambios", "material-history", bloque.changelog_md.splitlines())

    # 6. Interfaz de Variables
    if bloque.sections:
        var_lines = []
        for nombre_seccion, variables in bloque.sections.items():
            if not variables: continue
            var_lines.extend([
                f'**{nombre_seccion}**',
                '',  # Línea en blanco obligatoria antes de la tabla
                '| Nombre | Tipo | Retain | Valor Defecto | Comentario |',
                '| --- | --- | :---: | --- | --- |'
            ])
            for var in variables:
                com = var.comment if var.comment else "-"
                ret = "✔️" if var.is_retain else "-"
                var_lines.append(f'| `{var.name}` | `{var.data_type}` | {ret} | `{var.default_value}` | {com} |')
            var_lines.append('') # Espacio tras cada tabla
        add_card("Interfaz de Variables", "material-table-cog", var_lines)

    # 7. Código Fuente
    if bloque.source_code:
        code_lines = [
            '??? abstract "Desplegar Código SCL"',
            '    ```pascal'
        ]
        # Doble indentación: 4 espacios para la tarjeta (ya los pone add_card) + 4 espacios para que pertenezca al '???'
        for line in bloque.source_code.splitlines():
            code_lines.append(f'    {line}' if line.strip() else '    ')
        code_lines.append('    ```')
        
        add_card("Código Fuente Completo", "material-code-braces", code_lines)

    archivo_salida = output_dir / f"{bloque.name}.md"
    archivo_salida.write_text("\n".join(md_lines), encoding="utf-8")
    return archivo_salida