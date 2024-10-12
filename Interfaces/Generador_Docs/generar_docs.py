import os
from datetime import datetime
import json
from tkinter import Label, Entry, Button, Canvas, simpledialog, messagebox, Tk, filedialog
from docx import Document
from PIL import Image, ImageTk

# Paths and configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLANTILLA_PATH = os.path.join(BASE_DIR, 'Interfaces', 'Plantillas', 'CARTA DE PRES. 2024.docx')
IMAGEN_FONDO_PATH = os.path.join(BASE_DIR, 'Imagenes', 'fondodess.png')
CONTADOR_FILE = os.path.join(BASE_DIR, 'contador_documentos.json')

# UI Configuration
UI_CONFIG = {
    "window": {
        "title": "Generador de Documento DOCX estudiante",
        "width": 800,
        "height": 600
    },
    "background": {
        "image_path": IMAGEN_FONDO_PATH
    },
    "fields": [
        {"label": "Nombre:", "var_name": "entry_receptor", "x": 0.25, "y": 0.25},
        {"label": "Descripcion:", "var_name": "entry_descripcion", "x": 0.25, "y": 0.35},
        {"label": "Nombre Alumno:", "var_name": "entry_nombre_alumno", "x": 0.25, "y": 0.45},
        {"label": "Numero de Modulo:", "var_name": "entry_nu_modulo", "x": 0.25, "y": 0.55},
        {"label": "Nombre Modulo:", "var_name": "entry_nombre_modulo", "x": 0.25, "y": 0.65},
        {"label": "Horas de Modulo:", "var_name": "entry_horas_modulo", "x": 0.25, "y": 0.75}
    ],
    "buttons": {
        "generate": {"text": "Generar Documento", "x": 0.5, "y": 0.85},
        "reset": {"text": "Restablecer Contador", "x": 0.95, "y": 0.05}
    },
    "styles": {
        "label": {"font": ("Helvetica", 12), "fg": "white", "bg": "#2b2b2b"},
        "entry": {"font": ("Helvetica", 12), "width": 40},
        "button": {"font": ("Helvetica", 14), "cursor": "hand2"}
    }
}

# Document handling functions (unchanged)
def cargar_plantilla(ruta_plantilla):
    try:
        return Document(ruta_plantilla)
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar la plantilla: {e}")
        return None

def reemplazar_marcadores(doc, marcadores):
    for parrafo in doc.paragraphs:
        for marcador, valor in marcadores.items():
            if marcador in parrafo.text:
                parrafo.text = parrafo.text.replace(marcador, valor)
    for tabla in doc.tables:
        for fila in tabla.rows:
            for celda in fila.cells:
                for marcador, valor in marcadores.items():
                    if marcador in celda.text:
                        celda.text = celda.text.replace(marcador, valor)

def guardar_documento(doc, ruta_salida):
    try:
        doc.save(ruta_salida)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar el documento: {e}")
        return False

def obtener_ultimo_numero():
    try:
        if os.path.exists(CONTADOR_FILE):
            with open(CONTADOR_FILE, 'r') as f:
                data = json.load(f)
                return data.get('ultimo_anio', datetime.now().year), data.get('ultimo_numero', 0)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo de contador: {e}")
    return datetime.now().year, 0

def guardar_ultimo_numero(anio, numero):
    try:
        with open(CONTADOR_FILE, 'w') as f:
            json.dump({'ultimo_anio': anio, 'ultimo_numero': numero}, f)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el número de secuencia: {e}")
        return False

# Main function to generate the document
def generar_documento(entradas):
    fecha_actual = datetime.now()
    documento_original = cargar_plantilla(PLANTILLA_PATH)
    if not documento_original:
        return

    ultimo_anio, ultimo_numero = obtener_ultimo_numero()

    # Reset counter if the year changes or if it's 2025 or later
    if fecha_actual.year != ultimo_anio or fecha_actual.year >= 2025:
        nuevo_numero = 1
    else:
        nuevo_numero = ultimo_numero + 1
    
    numero_secuencia_str = f"{nuevo_numero:04}"

    datos = {
        '{Fecha}': fecha_actual.strftime('%d de %B %Y'),
        '{numero}': numero_secuencia_str,
        '{Anho}': str(fecha_actual.year),
        '{Nombre_Receptor}': entradas['entry_receptor'].get(),
        '{Descripcion}': entradas['entry_descripcion'].get(),
        '{Nombre_Alumno}': entradas['entry_nombre_alumno'].get(),
        '{N_Modulo}': entradas['entry_nu_modulo'].get(),
        '{Nombre_Modulo}': entradas['entry_nombre_modulo'].get(),
        '{Horas_Modulo}': entradas['entry_horas_modulo'].get()
    }

    nombre_archivo = simpledialog.askstring("Guardar como", "Introduce el nombre del archivo (sin extensión):")
    if not nombre_archivo:
        return 

    nombre_archivo = nombre_archivo.strip().replace(' ', '_')

    # Ask user for save directory
    directorio_destino = filedialog.askdirectory(title="Seleccionar directorio para guardar el documento")
    if not directorio_destino:
        return  # User cancelled the directory selection

    ruta_salida = os.path.join(directorio_destino, f'{nombre_archivo}.docx')

    contador = 1
    while os.path.exists(ruta_salida):
        ruta_salida = os.path.join(directorio_destino, f'{nombre_archivo}_{contador}.docx')
        contador += 1

    documento_copia = Document(PLANTILLA_PATH)
    reemplazar_marcadores(documento_copia, datos)

    if guardar_documento(documento_copia, ruta_salida):
        messagebox.showinfo("Éxito", f"Documento guardado como {ruta_salida}")
        if guardar_ultimo_numero(fecha_actual.year, nuevo_numero):
            messagebox.showinfo("Éxito", f"Número de secuencia actualizado: {nuevo_numero:04}")
        else:
            messagebox.showerror("Error", "No se pudo actualizar el número de secuencia.")

# Function to reset the counter to 0
def restablecer_contador():
    respuesta = messagebox.askyesno("Confirmación", "¿Está seguro de que desea restablecer el contador a 0?")
    if respuesta:
        try:
            with open(CONTADOR_FILE, 'w') as f:
                json.dump({'ultimo_anio': datetime.now().year, 'ultimo_numero': 0}, f)
            messagebox.showinfo("Éxito", "Contador restablecido a 0 para el año actual.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo restablecer el contador: {e}")

# GUI functions
def centro_ventana(ventana, ancho, alto):
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def crear_interfaz(root):
    config = UI_CONFIG
    root.title(config["window"]["title"])
    centro_ventana(root, config["window"]["width"], config["window"]["height"])
    
    # Load and resize the background image
    try:
        imagen_fondo = Image.open(config["background"]["image_path"])
        imagen_fondo = imagen_fondo.resize((config["window"]["width"], config["window"]["height"]))
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")
        imagen_fondo_tk = None

    # Create a canvas to display the background image
    canvas = Canvas(root, width=config["window"]["width"], height=config["window"]["height"], bd=0, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    if imagen_fondo_tk:
        canvas.create_image(0, 0, image=imagen_fondo_tk, anchor="nw")
        canvas.imagen_fondo_tk = imagen_fondo_tk  # Keep a reference to the image object

    # Create labels and input fields dynamically
    entradas = {}
    for field in config["fields"]:
        label = Label(canvas, text=field["label"], **config["styles"]["label"])
        canvas.create_window(field["x"] * config["window"]["width"], field["y"] * config["window"]["height"], window=label, anchor="e")

        entry = Entry(canvas, **config["styles"]["entry"])
        canvas.create_window((field["x"] + 0.05) * config["window"]["width"], field["y"] * config["window"]["height"], window=entry, anchor="w")
        entradas[field["var_name"]] = entry

    # Buttons
    btn_generar = Button(canvas, text=config["buttons"]["generate"]["text"], command=lambda: generar_documento(entradas), **config["styles"]["button"])
    canvas.create_window(config["buttons"]["generate"]["x"] * config["window"]["width"], 
                         config["buttons"]["generate"]["y"] * config["window"]["height"], 
                        window=btn_generar, anchor="center")

    btn_restablecer = Button(root, text=config["buttons"]["reset"]["text"], command=restablecer_contador, **config["styles"]["button"])
    btn_restablecer.place(relx=config["buttons"]["reset"]["x"], rely=config["buttons"]["reset"]["y"], anchor='ne')

    root.mainloop()

if __name__ == "__main__":
    root = Tk()
    crear_interfaz(root)