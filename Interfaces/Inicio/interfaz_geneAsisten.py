from tkinter import *
from tkinter import messagebox  # Importar messagebox para mostrar mensajes
from PIL import Image, ImageTk
from tkinter import ttk

# Crear la ventana principal
raiz = Tk()
raiz.resizable(False, False)
raiz.geometry('600x600')

# Cargar la imagen de fondo
imagen = Image.open(r'C:\Users\lloyd\Documents\entornos virtuales de python\Proyecto\Interfaces\Imagenes\fondo3.png')
imagen = imagen.resize((250, 560), Image.Resampling.LANCZOS)
imagen_fondo = ImageTk.PhotoImage(imagen)

# Crear un canvas para la imagen de fondo
canvas = Canvas(raiz, width=250, height=560)
canvas.grid(row=0, column=0, sticky='nw')  # 'sticky' asegura que se ajuste a la esquina superior izquierda
canvas.create_image(0, 0, image=imagen_fondo, anchor='nw')
canvas.image = imagen_fondo

# Título "LOGIN" en el canvas
canvas.create_text(280, 30, text='Generador de asistencia', font=('Broadway', 25,'bold'), fill="black")
#canvas.create_text(200, 150, text="Usuario:", font=('Arial', 18, 'bold'), fill='white')
#canvas.create_text(180, 265, text="Contraseña:", font=('Arial', 18, 'bold'), fill='white')
combobox = ttk.Combobox(raiz, value=['uno','dos','tres'], state='readonly') 
combobox.grid(row=0, column=1,columnspan=1, padx=10, pady=10)

boton_ingresar = Button(raiz, text="buscar", font=('Arial', 14), )
boton_ingresar.grid(row=0, column=1,columnspan=2, padx=10, pady=10)

boton_salir = Button(raiz, text="Cerrar", font=('Arial', 14), command=raiz.quit)
boton_salir.grid(row=0, column=1,columnspan=3, padx=10, pady=10)

raiz.mainloop()