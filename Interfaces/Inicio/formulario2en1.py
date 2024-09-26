import tkinter as tk
from tkinter import *
from tkinter import messagebox  # Importar messagebox para mostrar mensajes

from tkinter import ttk

class MainForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario Combinado")

        # Crear un marco para el primer formulario
        frame1 = tk.Frame(self.root, padx=10, pady=10)
        frame1.grid(row=0, column=0)

        imagen = Image.open(r'C:\Users\lloyd\Documents\entornos virtuales de python\Proyecto\Interfaces\Imagenes\fondo3.png')
        imagen = imagen.resize((250, 560), Image.Resampling.LANCZOS)
        imagen_fondo = ImageTk.PhotoImage(imagen)

# Crear un canvas para la imagen de fondo
        canvas = Canvas(frame1, width=250, height=560)
        canvas.grid(row=0, column=0, sticky='nw')  # 'sticky' asegura que se ajuste a la esquina superior izquierda
        canvas.create_image(0, 0, image=imagen_fondo, anchor='nw')
        canvas.image = imagen_fondo

# Título "LOGIN" en el canvas
        canvas.create_text(130, 30, text='GENERADOR', font=('Broadway', 15,'bold'), fill="white")
        canvas.create_text(150, 80, text="DE ", font=('Broadway', 15, 'bold'), fill='white')
        canvas.create_text(130, 130, text="ASISTENCIA", font=('Broadway', 15, 'bold'), fill='white')
    

        # Crear un marco para el segundo formulario
        frame2 = tk.Frame(self.root, padx=10, pady=10)
        frame2.grid(row=0, column=1)

        combobox = ttk.Combobox(frame2, value=['uno','dos','tres'], state='readonly') 
        combobox.grid(row=0, column=1,columnspan=1, padx=10, pady=10)

root = tk.Tk()
app = MainForm(root)
root.mainloop()
