import tkinter as tk
from tkinter import filedialog, messagebox

def inicializar_ui():
    """Oculta la ventana principal de Tkinter."""
    root = tk.Tk()
    root.withdraw()
    return root

def seleccionar_archivo_origen():
    """Abre un diálogo para seleccionar el archivo Word."""
    return filedialog.askopenfilename(
        title="1. Selecciona el Manual del Estándar (.docx)",
        filetypes=[("Documentos de Word", "*.docx"), ("Todos los archivos", "*.*")]
    )

def seleccionar_carpeta_destino():
    """Abre un diálogo para elegir la CARPETA donde se creará la ayuda."""
    return filedialog.askdirectory(
        title="2. Selecciona la carpeta de destino para la Ayuda Web"
    )

def mostrar_exito(mensaje):
    messagebox.showinfo("Proceso completado", mensaje)

def mostrar_error(mensaje):
    messagebox.showerror("Error crítico", mensaje)