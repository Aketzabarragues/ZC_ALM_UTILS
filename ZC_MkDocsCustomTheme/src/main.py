# src/main.py
import os
from pathlib import Path
import typer
from pydantic import ValidationError

from domain.models import BlockType
from extractors.data_parser import parsear_archivo_datos
from extractors.scl_parser import parsear_scl
from renderers.md_generator import generar_markdown_bloque

app = typer.Typer(help="Generador de Documentación ZC ALM", no_args_is_help=True)

@app.callback()
def main_callback() -> None:
    pass

@app.command()
def build(
    word_path: str = typer.Option(None, "--word", help="Ruta al manual Word (Pendiente de integrar)"),
    scl_path: str = typer.Option(..., "--fuentes", help="Ruta a la carpeta con archivos SCL/DB/UDT"),
    docs_dir: Path = typer.Option(Path("./docs"), "--out", help="Carpeta salida de MkDocs")
) -> None:
    
    docs_dir.mkdir(parents=True, exist_ok=True)
    fuentes_dir = Path(scl_path)
    
    if not fuentes_dir.exists() or not fuentes_dir.is_dir():
        typer.secho(f"[-] Directorio de fuentes inválido: {scl_path}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    try:
        # Escaneo de todos los archivos de Siemens
        archivos_fuente = list(fuentes_dir.glob("*.db")) + list(fuentes_dir.glob("*.udt")) + list(fuentes_dir.glob("*.scl"))
        total_bloques = 0
        
        for archivo in archivos_fuente:
            bloques_extraidos = []
            
            # Enrutamiento al Extractor adecuado
            if archivo.suffix.lower() == '.scl':
                try:
                    bloques_extraidos.append(parsear_scl(archivo))
                except Exception as e:
                    typer.secho(f"[-] Omitiendo SCL {archivo.name}: {e}", fg=typer.colors.YELLOW)
            else:
                bloques_extraidos.extend(parsear_archivo_datos(archivo))
            
            # Renderizado y Generación de Markdown
            for bloque in bloques_extraidos:
                # Carpetas que MkDocs usará para el menú lateral
                if bloque.block_type in [BlockType.FC, BlockType.FB]:
                    carpeta_destino = docs_dir / "Bloques de codigo"
                else:
                    carpeta_destino = docs_dir / "Estructura de datos"
                
                carpeta_destino.mkdir(parents=True, exist_ok=True)
                ruta_generada = generar_markdown_bloque(bloque, carpeta_destino)
                typer.echo(f"[+] Generado: {ruta_generada}")
                total_bloques += 1

        # Crear el index.md básico si no existe
        index_path = docs_dir / "index.md"
        if not index_path.exists():
            index_path.write_text("# Documentación ZC ALM\n\nBienvenido a la documentación técnica generada automáticamente.", encoding="utf-8")

        typer.secho(f"\n[OK] Escaneo finalizado. {total_bloques} bloques listos para MkDocs.", fg=typer.colors.GREEN)
        
    except ValidationError as e:
        typer.secho(f"[X] Error crítico de validación Pydantic:\n{e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()