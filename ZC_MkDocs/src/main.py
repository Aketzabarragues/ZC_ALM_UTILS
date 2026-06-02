import os
from pathlib import Path
import typer
from pydantic import ValidationError
from domain.models import BlockType

# Importación de Extractores y Renderizadores
from extractors.tia_parser import parsear_archivo_datos
from extractors.scl_parser import parsear_scl
from renderers.md_generator import generar_markdown_bloque

app = typer.Typer(help="Generador de Documentación ZC ALM", no_args_is_help=True)

@app.callback()
def main_callback() -> None:
    pass

@app.command()
def build(
    word_path: str = typer.Option(..., "--word", help="Ruta al manual Word"),
    scl_path: str = typer.Option(..., "--fuentes", help="Ruta a fuentes SCL/DB"),
    docs_dir: Path = typer.Option(Path("./docs"), "--out", help="Carpeta salida MD")
) -> None:
    
    docs_dir.mkdir(parents=True, exist_ok=True)
    fuentes_dir = Path(scl_path)
    
    if not fuentes_dir.exists() or not fuentes_dir.is_dir():
        typer.secho(f"Directorio de fuentes inválido: {scl_path}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    try:
        archivos_fuente = list(fuentes_dir.glob("*.db")) + list(fuentes_dir.glob("*.udt")) + list(fuentes_dir.glob("*.scl"))
        total_bloques = 0
        
        for archivo in archivos_fuente:
            bloques_extraidos = []
            if archivo.suffix.lower() == '.scl':
                try:
                    bloques_extraidos.append(parsear_scl(archivo))
                except Exception as e:
                    typer.secho(f"[-] Omitiendo {archivo.name}: {e}", fg=typer.colors.YELLOW)
            else:
                bloques_extraidos.extend(parsear_archivo_datos(archivo))
            
            for bloque in bloques_extraidos:
                # Adaptación al vuelo de DB/UDT
                if not bloque.sections and hasattr(bloque, 'variables'):
                    bloque.sections = {"Variables": bloque.variables}
                
                # Enrutador físico con los nombres EXACTOS para el menú automático
                if bloque.block_type in [BlockType.FC, BlockType.FB]:
                    carpeta_destino = docs_dir / "Bloques de codigo"
                else:  # DB y UDT
                    carpeta_destino = docs_dir / "Estructura de datos"
                
                carpeta_destino.mkdir(parents=True, exist_ok=True)
                ruta_generada = generar_markdown_bloque(bloque, carpeta_destino)
                
                typer.echo(f"[+] Generado: {ruta_generada}")
                total_bloques += 1

        typer.secho(f"Escaneo finalizado. {total_bloques} bloques procesados.", fg=typer.colors.GREEN)
        
    except ValidationError as e:
        typer.secho(f"Error crítico de validación:\n{e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()