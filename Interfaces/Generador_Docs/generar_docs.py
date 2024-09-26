from tkinter import *
from tkinter import simpledialog, messagebox
from docx import Document
from datetime import datetime
import os
from PIL import Image, ImageTk  
import json

# Función para cargar la plantilla de Word
def cargar_plantilla(ruta_plantilla):
    try:
        return Document(ruta_plantilla)
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar la plantilla: {e}")
        return None

# Función para reemplazar marcadores en el documento
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

# Función para guardar el documento final
def guardar_documento(doc, ruta_salida):
    try:
        doc.save(ruta_salida)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar el documento: {e}")
        return False

# Función para obtener el número de secuencia del documento original sin llaves
def obtener_ultimo_numero():
    archivo_contador = 'contador_documentos.json'
    try:
        if os.path.exists(archivo_contador):
            with open(archivo_contador, 'r') as f:
                data = json.load(f)
                return data.get('ultimo_numero', 0)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo de contador: {e}")
    return 0

# Función para guardar el último número de secuencia
def guardar_ultimo_numero(numero):
    archivo_contador = 'contador_documentos.json'
    try:
        with open(archivo_contador, 'w') as f:
            json.dump({'ultimo_numero': numero}, f)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el número de secuencia: {e}")
        return False

# Función para recoger los datos y generar el documento
def generar_documento():
    fecha_actual = datetime.now().strftime('%d de %B %Y')
    ruta_plantilla = r'C:\Users\lloyd\Documents\entornos virtuales de python\Proyecto\Interfaces\Plantillas\word1.docx'
    
    documento_original = cargar_plantilla(ruta_plantilla)
    if not documento_original:
        return

    ultimo_numero = obtener_ultimo_numero()
    nuevo_numero = ultimo_numero + 1
    numero_secuencia_str = f"{nuevo_numero:04}"

    datos = {
        '{nombre}': entry_nombre.get(),
        '{dni}': entry_dni.get(),
        '{universidad}': entry_universidad.get(),
        '{carrera}': entry_carrera.get(),
        '{empresa}': entry_empresa.get(),
        '{fecha_inicio}': entry_fecha_inicio.get(),
        '{fecha_fin}': entry_fecha_fin.get(),
        '{fecha_actual}': fecha_actual,
        '{telefono}': entry_telefono.get(),
        '{email}': entry_email.get(),
        '{ciudad}': entry_ciudad.get(),
        '{numero}': numero_secuencia_str,
    }

    nombre_archivo = simpledialog.askstring("Guardar como", "Introduce el nombre del archivo (sin extensión):")
    if not nombre_archivo:
        return 

    nombre_archivo = nombre_archivo.strip().replace(' ', '_')
    ruta_salida = f'{nombre_archivo}.docx'

    contador = 1
    while os.path.exists(ruta_salida):
        ruta_salida = f'{nombre_archivo}_{contador}.docx'
        contador += 1

    documento_copia = Document(ruta_plantilla)

    reemplazar_marcadores(documento_copia, datos)
    if guardar_documento(documento_copia, ruta_salida):
        messagebox.showinfo("Éxito", f"Documento guardado como {ruta_salida}")
        if guardar_ultimo_numero(nuevo_numero):
            messagebox.showinfo("Éxito", f"Número de secuencia actualizado: {nuevo_numero:04}")
        else:
            messagebox.showerror("Error", "No se pudo actualizar el número de secuencia.")

#funcion para reestablecer el contador a 0
def restablecer_contador():
    # Preguntar al usuario si está seguro de restablecer el contador
    respuesta = messagebox.askyesno("Confirmación", "¿Está seguro de que desea restablecer el contador a 0?")
    
    if respuesta:  # Si el usuario elige "Sí"
        archivo_contador = 'contador_documentos.json'
        try:
            with open(archivo_contador, 'w') as f:
                json.dump({'ultimo_numero': 0}, f)
            messagebox.showinfo("Éxito", "Contador restablecido a 0.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo restablecer el contador: {e}")

#esto es para poner la ventana en el medio de la pantalla
def centro_ventana(ventana,ancho,alto):
    x=(ventana.winfo_screenwidth()-ancho)/2
    y=(ventana.winfo_screenheight()-alto)/2
    ventana.geometry(f"{ancho}x{alto}+{int(x)}+{int(y)}")

# Interfaz gráfica
raiz = Tk()
raiz.title('Generador de Documento DOCX estudiante')
# raiz.geometry('600x600')
ancho = 600
alto = 600

centro_ventana(raiz,ancho,alto)
# Cargar y redimensionar la imagen de fondo
ruta_imagen = r'C:\Users\lloyd\Documents\entornos virtuales de python\Proyecto\Interfaces\Imagenes\fondo1.jpg' 
imagen_fondo = Image.open(ruta_imagen)
imagen_fondo = imagen_fondo.resize((600, 600)) 
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

# Crear un canvas para mostrar la imagen de fondo
canvas = Canvas(raiz, width=600, height=600)
canvas.pack(fill="both", expand=True)

# Cambiar el borde 
canvas.config(bd=15) 
canvas.config(relief='groove')
canvas.config(cursor='arrow') 

# Colocar imagen de fondo 
canvas.create_image(0, 0, image=imagen_fondo, anchor="nw")

# Crear un Label como contenedor con fondo igual al de la ventana
contenedor = Label(canvas)  
contenedor.place(relx=0.5, rely=0.5, anchor="center") 

# Lista de campos y variables de entrada
campos = [
    ("Nombre:", "entry_nombre"),
    ("DNI:", "entry_dni"),
    ("Universidad:", "entry_universidad"),
    ("Carrera:", "entry_carrera"),
    ("Empresa:", "entry_empresa"),
    ("Fecha inicio:", "entry_fecha_inicio"),
    ("Fecha final:", "entry_fecha_fin"),
    ("Teléfono:", "entry_telefono"),
    ("Email:", "entry_email"),
    ("Ciudad:", "entry_ciudad")
]

# Crear etiquetas y campos de entrada dinámicamente
entradas = {}
for i, (label_text, var_name) in enumerate(campos):
    label = Label(contenedor, text=label_text, font=("Helvetica", 12), foreground="black", background="white")
    label.grid(row=i, column=0, padx=10, pady=5, sticky='w')

    entry = Entry(contenedor, width=40, font=("Helvetica", 12))
    entry.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
    entradas[var_name] = entry

# Asignar las entradas a variables globales
entry_nombre = entradas['entry_nombre']
entry_dni = entradas['entry_dni']
entry_universidad = entradas['entry_universidad']
entry_carrera = entradas['entry_carrera']
entry_empresa = entradas['entry_empresa']
entry_fecha_inicio = entradas['entry_fecha_inicio']
entry_fecha_fin = entradas['entry_fecha_fin']
entry_telefono = entradas['entry_telefono']
entry_email = entradas['entry_email']
entry_ciudad = entradas['entry_ciudad']

# Botón para generar el documento
btn_generar = Button(contenedor, text="Generar Documento", command=generar_documento, font=("Helvetica", 14),cursor="hand2")
btn_generar.grid(row=len(campos), columnspan=2, pady=20)

#boton para reestablecer el contador a 0
btn_restablecer = Button(raiz, text="Restablecer Contador", command=restablecer_contador, font=("Helvetica", 14),cursor="hand2")
btn_restablecer.place(relx=0.95, y=10, anchor='ne')

raiz.mainloop()
# if __name__ == "__main__":
#     raiz.mainloop()