import tkinter as tk
from tkinter import messagebox  # Importar messagebox para mostrar mensajes
from PIL import Image, ImageTk
import sys
import os
from tkinter import ttk

# Añadir la carpeta raíz del proyecto al PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

class MainForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario Combinado")

        # Crear un marco para el primer formulario
        frame1 = tk.Frame(self.root, padx=10, pady=10)
        frame1.grid(row=0, column=0)

        # Cargar la imagen de fondo
        imagen_path = os.path.join(project_root, "Imagenes", "fondo1.jpg")  # Ajusta esta ruta según tu estructura de carpetas
        
        # Verificar si la imagen existe antes de intentar abrirla
        if not os.path.exists(imagen_path):
            messagebox.showerror("Error", f"No se encontró la imagen en: {imagen_path}")
            self.root.destroy()  # Cerrar la ventana si no se encuentra la imagen
            return
        
        imagen = Image.open(imagen_path)  # Abrir la imagen con PIL
        imagen = imagen.resize((250, 560), Image.LANCZOS)  # Ajustar el tamaño de la imagen
        imagen_fondo = ImageTk.PhotoImage(imagen)

        # Crear un canvas para la imagen de fondo
        canvas = tk.Canvas(frame1, width=250, height=560)
        canvas.grid(row=0, column=0, sticky='nw')  # 'sticky' asegura que se ajuste a la esquina superior izquierda
        canvas.create_image(0, 0, image=imagen_fondo, anchor='nw')
        canvas.image = imagen_fondo

        # Títulos en el canvas
        canvas.create_text(130, 30, text='GENERADOR', font=('Broadway', 15,'bold'), fill="white")
        canvas.create_text(150, 80, text="DE ", font=('Broadway', 15, 'bold'), fill='white')
        canvas.create_text(130, 130, text="ASISTENCIA", font=('Broadway', 15, 'bold'), fill='white')
    
        # Crear un marco para el segundo formulario
        frame2 = tk.Frame(self.root, padx=10, pady=10)
        frame2.grid(row=0, column=1)

        # Crear un combobox en el segundo marco
        combobox = ttk.Combobox(frame2, values=['uno', 'dos', 'tres'], state='readonly') 
        combobox.grid(row=0, column=0, padx=10, pady=10)  # Ajustar la posición del combobox

# Crear la ventana principal y ejecutar la aplicación
root = tk.Tk()
app = MainForm(root)
root.mainloop()