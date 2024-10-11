import tkinter as tk
from tkinter import ttk
import sys
import os

# Get the path of the current directory (where menu_principal.py is located)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the path of the parent directory (the project directory)
parent_dir = os.path.dirname(current_dir)

# Add the project directory to sys.path
sys.path.append(parent_dir)

# Add the Excel_a_Sql folder to sys.path
excel_sql_path = os.path.join(parent_dir, 'Excel_a_Sql')
sys.path.append(excel_sql_path)

# Now we try to import the modules
try:
    from Generador_Docs.generar_docs import crear_interfaz
    from Excel_a_Sql.excel_sql_id import ExcelToMySQLConverter
except ImportError as e:
    print(f"Error importing module: {e}")
    print(f"sys.path: {sys.path}")
    sys.exit(1)

def abrir_generador():
    root = tk.Toplevel()
    crear_interfaz(root)

def abrir_excel_a_sql():
    converter = ExcelToMySQLConverter()
    converter.run()

def abrir_menu_principal():
    menu = tk.Tk()
    menu.title("Menú Principal")
    menu.overrideredirect(True)

    # Center the window
    ancho = 400
    alto = 300
    x = (menu.winfo_screenwidth() - ancho) // 2
    y = (menu.winfo_screenheight() - alto) // 2
    menu.geometry(f"{ancho}x{alto}+{x}+{y}")
    def cerrar():
        menu.destroy()
    # Main menu title
    label_menu = ttk.Label(menu, text="Bienvenido al Menú Principal", font=("Arial", 16, "bold"))
    label_menu.pack(pady=20)

    # Button to open the document generator
    btn_opcion1 = ttk.Button(menu, text="Abrir Generador", command=abrir_generador)
    btn_opcion1.pack(pady=10)

    # Button to open Excel to SQL
    btn_opcion2 = ttk.Button(menu, text="Excel a SQL", command=abrir_excel_a_sql)
    btn_opcion2.pack(pady=10)
    btn_cerrar = ttk.Button(menu, text="Cerrar", command=cerrar)
    btn_cerrar.pack(pady=10)

    menu.mainloop()

if __name__ == "__main__":
    abrir_menu_principal()