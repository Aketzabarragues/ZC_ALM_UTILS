from pathlib import Path
from domain.models import SiemensBlock

def generar_markdown_bloque(bloque: SiemensBlock, output_dir: Path) -> Path:
    md_lines = [
        "---",
        f"title: {bloque.name}",
        "---",
        f"# {bloque.block_type.value} {bloque.name}",
        ""
    ]
    
    # 1. Admonition: Información del Sistema
    md_lines.extend([
        '!!! info "Información del Sistema"',
        f"    **Hardware:** {bloque.system_info.hardware or '-'}<br>",
        f"    **Ingeniería:** {bloque.system_info.engineering or '-'}<br>",
        f"    **Versión:** {bloque.version or '-'}<br>",
        f"    **Autor:** {bloque.author or '-'}",
        ""
    ])

    # 2. Admonition: Restricciones
    if bloque.restrictions and bloque.restrictions.lower() != "ninguna.":
        md_lines.extend([
            '!!! warning "Restricciones"',
            f"    {bloque.restrictions}",
            ""
        ])
    else:
        md_lines.extend([
            '!!! note "Restricciones"',
            "    Ninguna restricción operativa detectada.",
            ""
        ])
        
    # 3. Descripción Funcional
    if bloque.description:
        md_lines.extend([
            "## Descripción Funcional",
            bloque.description,
            ""
        ])

    # 4. Admonition: Dependencias
    if bloque.dependencies:
        all_links = []
        for dep in bloque.dependencies:
            elements_clean = [e.strip().replace('`', '') for e in dep.elements.split(',')]
            for e in elements_clean:
                if e == "-": continue
                if e.startswith("FC") or e.startswith("FB"):
                    all_links.append(f"    **FC:** [{e}](../Bloques de codigo/{e}.md)")
                else:
                    all_links.append(f"    **DB:** [{e}](../Estructura de datos/{e}.md)")
        
        if all_links:
            md_lines.append('!!! abstract "Dependencias Requeridas"')
            md_lines.extend(all_links)
            md_lines.append("")

    # 5. Interfaz de Variables
    if bloque.sections:
        md_lines.append("## Interfaz de Variables")
        for nombre_seccion, variables in bloque.sections.items():
            if not variables: continue
            md_lines.extend([
                f"### {nombre_seccion}",
                "| Nombre | Tipo | Retain | Valor Defecto | Comentario |",
                "|---|---|:---:|---|---|"
            ])
            for var in variables:
                com = var.comment if var.comment else "-"
                ret = "✔️" if var.is_retain else "-"
                md_lines.append(f"| `{var.name}` | `{var.data_type}` | {ret} | `{var.default_value}` | {com} |")
            md_lines.append("")

    # 6. Historial de Cambios
    if bloque.changelog_md:
        md_lines.extend([
            "## Historial de Cambios", 
            bloque.changelog_md, 
            ""
        ])
        
    # 7. Código Fuente Colapsable (Fix para bug del footer en Shadcn)
    if bloque.source_code:
        md_lines.extend([
            "## Código Fuente",
            '<details class="group rounded-xl border bg-card p-4 shadow-sm">',
            '<summary class="font-semibold cursor-pointer">Desplegar Código SCL</summary>',
            '<div class="mt-4" markdown>',
            '',
            '```pascal'
        ])
        for linea in bloque.source_code.splitlines():
            md_lines.append(linea)
        md_lines.extend([
            '```',
            '',
            '</div>',
            '</details>',
            '<div class="h-24"></div>'  # Spacer esencial para proteger el footer
        ])

    archivo_salida = output_dir / f"{bloque.name}.md"
    archivo_salida.write_text("\n".join(md_lines), encoding="utf-8")
    return archivo_salida