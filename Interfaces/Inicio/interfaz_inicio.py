from tkinter import *
from tkinter import messagebox  
from PIL import Image, ImageTk
import sys
import os

# Añadir la carpeta raíz del proyecto al PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# Crear la ventana principal
raiz = Tk()
raiz.config(bd=20, relief='ridge')
raiz.resizable(False, False)

# Centrar la ventana
ancho = 600
alto = 600
raiz.geometry(f"{ancho}x{alto}")

an_vent = raiz.winfo_screenwidth()
alt_vent = raiz.winfo_screenheight()

x = (an_vent // 2) - (ancho // 2)
y = (alt_vent // 2) - (alto // 2)

raiz.geometry(f"{ancho}x{alto}+{x}+{y}")

# Variables para almacenar el usuario y la contraseña
Nombre = StringVar()
Apellido = StringVar()

# Cargar la imagen de fondo
imagen_path = os.path.join(project_root, "Imagenes", "fondodess.png")  # Ajusta esta ruta según tu estructura de carpetas

# Verificar si la imagen existe antes de intentar abrirla
if not os.path.exists(imagen_path):
    messagebox.showerror("Error", f"No se encontró la imagen en: {imagen_path}")
    raiz.destroy()  # Cerrar la ventana si no se encuentra la imagen
else:
    imagen = Image.open(imagen_path)  # Abrir la imagen con PIL
    imagen = imagen.resize((560, 560), Image.LANCZOS)  # Ajustar el tamaño de la imagen
    imagen_fondo = ImageTk.PhotoImage(imagen)

    # Crear un canvas para la imagen de fondo
    canvas = Canvas(raiz, width=560, height=560)
    canvas.grid(row=0, column=0, columnspan=3, rowspan=5)
    canvas.create_image(0, 0, image=imagen_fondo, anchor='nw')
    canvas.image = imagen_fondo

# Título "LOGIN" en el canvas
canvas.create_text(280, 30, text='LOGIN', font=('Broadway', 25,'bold'), fill="white")
canvas.create_text(200, 150, text="Usuario:", font=('Arial', 18, 'bold'), fill='white')
canvas.create_text(180, 265, text="Contraseña:", font=('Arial', 18, 'bold'), fill='white')

# Crear los labels y entradas
usuario = Entry(raiz, font=('Arial', 14))
usuario.grid(row=1, column=2)

contraseña = Entry(raiz, font=('Arial', 14), show='*')
contraseña.grid(row=2, column=2)

# Función para verificar el usuario y la contraseña
def verificar_login():
    if usuario.get() == 'admin' and contraseña.get() == 'admin':
        messagebox.showinfo("Éxito", "¡Bienvenido!🙌😒👌")
    else:
        messagebox.showerror("Error", "Pon bien credenciales o te bloqueo😘😍🤣.")

# Crear los botones
boton_ingresar = Button(raiz, text="Ingresar", font=('Arial', 14), command=verificar_login)
boton_ingresar.grid(row=3, column=0, padx=10, pady=10)

boton_salir = Button(raiz, text="Cerrar", font=('Arial', 14), command=raiz.quit)
boton_salir.grid(row=3, column=2, padx=10, pady=10)

raiz.mainloop()