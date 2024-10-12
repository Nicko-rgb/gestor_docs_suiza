import tkinter as tk
from tkinter import ttk
import sys
import os

# Configuración de rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
excel_sql_path = os.path.join(parent_dir, 'Excel_a_Sql')

sys.path.append(parent_dir)
sys.path.append(excel_sql_path)

# Importaciones de módulos
try:
    from Generador_Docs.generar_docs import crear_interfaz
    from Excel_a_Sql.excel_sql_id import ExcelToMySQLConverter
except ImportError as e:
    print(f"Error importing module: {e}")
    print(f"sys.path: {sys.path}")
    sys.exit(1)

def configurar_estilos():
    style = ttk.Style()
    style.theme_use('clam')

    # Estilos generales
    style.configure('TFrame', background='#F0F4F8')
    style.configure('TLabel', background='#F0F4F8', foreground='#2D3748', font=('Segoe UI', 12))
    style.configure('TButton', font=('Segoe UI', 10))
    
    # Estilo para el título
    style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), foreground='#2D3748')
    
    # Estilos para las tarjetas
    style.configure('Card.TFrame', background='#FFFFFF', relief='flat')
    style.configure('CardTitle.TLabel', background='#FFFFFF', foreground='#2D3748', font=('Segoe UI', 16, 'bold'))
    style.configure('CardBody.TLabel', background='#FFFFFF', foreground='#4A5568', font=('Segoe UI', 10))
    style.configure('Card.TButton', background='#4299E1', foreground='white', font=('Segoe UI', 10, 'bold'))
    style.map('Card.TButton', background=[('active', '#3182CE')])

    # Estilos para los botones del pie de página
    style.configure('Footer.TButton', background='#E2E8F0', foreground='#4A5568', font=('Segoe UI', 9))
    style.map('Footer.TButton', background=[('active', '#CBD5E0')])

def crear_tarjeta(parent, titulo, descripcion, comando):
    card = ttk.Frame(parent, style='Card.TFrame', padding=(20, 20, 20, 20))
    card.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    ttk.Label(card, text=titulo, style='CardTitle.TLabel').pack(pady=(0, 10))
    ttk.Label(card, text=descripcion, style='CardBody.TLabel', wraplength=200).pack(pady=(0, 20))
    ttk.Button(card, text="Abrir", style='Card.TButton', command=comando).pack()

def abrir_generador():
    root = tk.Toplevel()
    crear_interfaz(root)

def abrir_excel_a_sql():
    converter = ExcelToMySQLConverter()
    converter.run()

def regresar():
    print("Función 'Regresar' no implementada")

def abrir_menu_principal():
    menu = tk.Tk()
    menu.title("Sistema de Gestión Empresarial")
    configurar_estilos()

    #quitar la barra de arriba
    menu.overrideredirect(1)
    # Configuración de la ventana
    ancho, alto = 800, 600
    x = (menu.winfo_screenwidth() - ancho) // 2
    y = (menu.winfo_screenheight() - alto) // 2
    menu.geometry(f"{ancho}x{alto}+{x}+{y}")

    # Frame principal
    frame_principal = ttk.Frame(menu, padding="40 40 40 40")
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Título del menú principal
    ttk.Label(frame_principal, text="Panel de Control", style='Title.TLabel').pack(pady=(0, 40))

    # Frame para las tarjetas
    frame_tarjetas = ttk.Frame(frame_principal)
    frame_tarjetas.pack(fill=tk.BOTH, expand=True)

    # Crear tarjetas de opciones
    crear_tarjeta(frame_tarjetas, 
                  "Generador de Documentos", 
                  "Crea y gestiona documentos empresariales de manera eficiente.", 
                  abrir_generador)

    crear_tarjeta(frame_tarjetas, 
                  "Conversor Excel a SQL", 
                  "Convierte tus hojas de cálculo a bases de datos SQL con facilidad.", 
                  abrir_excel_a_sql)

    # Frame para el pie de página
    frame_footer = ttk.Frame(frame_principal)
    frame_footer.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))

    # Etiqueta de copyright
    ttk.Label(frame_footer, text="© 2024 Sistema de Gestión Empresarial", 
              font=('Segoe UI', 8)).pack(side=tk.LEFT)

    # Frame para los botones de acción
    frame_botones = ttk.Frame(frame_footer)
    frame_botones.pack(side=tk.RIGHT)

    # Botones de acción
    ttk.Button(frame_botones, text="Regresar", style='Footer.TButton', command=regresar).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(frame_botones, text="Cerrar", style='Footer.TButton', command=menu.quit).pack(side=tk.LEFT)

    menu.mainloop()

if __name__ == "__main__":
    abrir_menu_principal()