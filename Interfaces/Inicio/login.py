# login.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance
from menu_principal import abrir_menu_principal  # Importar la función del menú
import sys
import os
# Añadir la carpeta raíz del proyecto al PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

root = tk.Tk()
root.title("Login")

# Dimensiones de la ventana
ancho = 600
alto = 400

# Centrar la ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    x = (ventana.winfo_screenwidth() - ancho) / 2
    y = (ventana.winfo_screenheight() - alto) / 2
    ventana.geometry(f"{ancho}x{alto}+{int(x)}+{int(y)}")

centrar_ventana(root, ancho, alto)

# Cargar y ajustar la imagen de fondo
fondo = Image.open(r"C:\Users\lloyd\Documents\entornos virtuales de python\Proyecto\Interfaces\Imagenes\fondo1.jpg")
fondo = fondo.resize((ancho, alto), Image.LANCZOS)

# Oscurecer el fondo
enhancer = ImageEnhance.Brightness(fondo)
imagen_oscura = enhancer.enhance(0.4)

# Hacer el fondo ligeramente opaco
imagen_oscura = imagen_oscura.convert("RGBA")
alpha = Image.new("L", imagen_oscura.size, 240)  # Control de opacidad
imagen_oscura.putalpha(alpha)

# Convertir la imagen de fondo para usarla en tkinter
img_fondo = ImageTk.PhotoImage(imagen_oscura)

# Crear un label para la imagen de fondo
fondo_label = tk.Label(root, image=img_fondo)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

# Crear un Frame (cuadro) centrado para el formulario de login
frame_login = ttk.Frame(root, padding=20, style="Card.TFrame")
frame_login.place(relx=0.5, rely=0.5, anchor="center")  # Centrar el frame en la ventana

# Estilos personalizados para el Frame
style = ttk.Style()
style.configure("Card.TFrame", background="white", borderwidth=1, relief="solid")

# Encabezado del cuadro de login
label_encabezado = ttk.Label(frame_login, text="Login", font=("Arial", 16, "bold"), background="white")
label_encabezado.grid(row=0, columnspan=2, pady=(0, 10))

# Etiqueta y campo de texto para nombre de usuario
label_usuario = ttk.Label(frame_login, text="Usuario:", background="white")
label_usuario.grid(row=1, column=0, sticky="w", padx=5, pady=5)

entry_usuario = ttk.Entry(frame_login, width=30)
entry_usuario.grid(row=1, column=1, padx=5, pady=5)

# Etiqueta y campo de texto para contraseña
label_password = ttk.Label(frame_login, text="Contraseña:", background="white")
label_password.grid(row=2, column=0, sticky="w", padx=5, pady=5)

entry_password = ttk.Entry(frame_login, show="*", width=30)
entry_password.grid(row=2, column=1, padx=5, pady=5)

# Función para iniciar sesión
def iniciar_sesion():
    usuario = entry_usuario.get()
    contraseña = entry_password.get()
    
    # Aquí debes reemplazar con la lógica de verificación de credenciales
    if usuario == "admin" and contraseña == "1234":  # Cambia esto según sea necesario
        root.destroy()  # Cerrar la ventana de login
        abrir_menu_principal()  # Abrir el menú principal
    else:
        # Aquí puedes mostrar un mensaje de error
        error_label = ttk.Label(frame_login, text="Credenciales incorrectas.", foreground="red", background="white")
        error_label.grid(row=4, columnspan=2)

# Vincular la tecla Enter al campo de contraseña
entry_password.bind("<Return>", lambda event: iniciar_sesion())

# Botón para login
btn_login = ttk.Button(frame_login, text="Iniciar Sesión", command=iniciar_sesion)
btn_login.grid(row=3, columnspan=2, pady=10)

root.mainloop()
