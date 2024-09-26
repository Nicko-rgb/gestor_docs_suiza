import tkinter as tk
from tkinter import ttk
# from ..Generador_Docs.generar_docs import generar_docs  # Importación relativa

# def abrir_generador():
#     ventana_generador = tk.Toplevel()
#     ventana_generador.title("Generador de Documentos")
    
#     # Aquí puedes agregar el contenido del generador
#     label = ttk.Label(ventana_generador, text="Este es el generador de documentos.")
#     label.pack(pady=20)

def abrir_menu_principal():
    menu = tk.Tk()
    menu.title("Menú Principal")

    # Centrar la ventana
    ancho = 400
    alto = 300
    x = (menu.winfo_screenwidth() - ancho) / 2
    y = (menu.winfo_screenheight() - alto) / 2
    menu.geometry(f"{ancho}x{alto}+{int(x)}+{int(y)}")

    # Título del menú principal
    label_menu = ttk.Label(menu, text="Bienvenido al Menú Principal", font=("Arial", 16, "bold"))
    label_menu.pack(pady=20)

    # Botón para abrir el generador de documentos
    btn_opcion1 = ttk.Button(menu, text="Abrir Generador")
    btn_opcion1.pack(pady=10)

    btn_opcion2 = ttk.Button(menu, text="Opción 2")
    btn_opcion2.pack(pady=10)

    menu.mainloop()
