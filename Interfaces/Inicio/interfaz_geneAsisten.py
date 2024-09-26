from tkinter import *
from tkinter import messagebox  # Importar messagebox para mostrar mensajes
from PIL import Image, ImageTk
from tkinter import ttk
import sys
import os

# Añadir la carpeta raíz del proyecto al PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# Crear la ventana principal
raiz = Tk()
raiz.resizable(False, False)
raiz.geometry('600x600')

# Cargar la imagen de fondo
imagen_path = os.path.join(project_root, "Imagenes", "fondo1.jpg")  # Ajusta esta ruta según tu estructura de carpetas

# Verificar si la imagen existe antes de intentar abrirla
if not os.path.exists(imagen_path):
    messagebox.showerror("Error", f"No se encontró la imagen en: {imagen_path}")
    raiz.destroy()  # Cerrar la ventana si no se encuentra la imagen
else:
    imagen = Image.open(imagen_path)  # Abrir la imagen con PIL
    imagen = imagen.resize((250, 560), Image.LANCZOS)  # Ajustar el tamaño de la imagen
    imagen_fondo = ImageTk.PhotoImage(imagen)

    # Crear un canvas para la imagen de fondo
    canvas = Canvas(raiz, width=250, height=560)
    canvas.grid(row=0, column=0, sticky='nw')  # 'sticky' asegura que se ajuste a la esquina superior izquierda
    canvas.create_image(0, 0, image=imagen_fondo, anchor='nw')
    canvas.image = imagen_fondo

# Título en el canvas
canvas.create_text(130, 30, text='Generador de asistencia', font=('Broadway', 25,'bold'), fill="black")

# Combobox
combobox = ttk.Combobox(raiz, values=['uno', 'dos', 'tres'], state='readonly') 
combobox.grid(row=0, column=1, padx=10, pady=10)

# Botón para buscar
boton_ingresar = Button(raiz, text="Buscar", font=('Arial', 14), command=lambda: buscar(combobox.get()))
boton_ingresar.grid(row=1, column=1, padx=10, pady=10)

# Botón para cerrar
boton_salir = Button(raiz, text="Cerrar", font=('Arial', 14), command=raiz.quit)
boton_salir.grid(row=2, column=1, padx=10, pady=10)

def buscar(opcion):
    messagebox.showinfo("Buscar", f"Buscando: {opcion}")

raiz.mainloop()