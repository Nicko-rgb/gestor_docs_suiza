import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Función para crear la ventana de configuración
def abrir_configuracion():
    def guardar_configuracion():
        global host, usuario, password, bd
        host = entry_host.get()
        usuario = entry_usuario.get()
        password = entry_password.get()
        bd = entry_base_datos.get()
        
        config_window.destroy()

    # Crear la ventana de configuración
    config_window = tk.Toplevel(root)
    config_window.title("Configuración de conexión")
    config_window.geometry("320x220")

    # Estilo para el contenido
    padding_x = 10
    padding_y = 10

    ttk.Label(config_window, text="Host:").grid(column=0, row=0, sticky=tk.W, padx=padding_x, pady=padding_y)
    entry_host = ttk.Entry(config_window, width=30)
    entry_host.grid(column=1, row=0, padx=padding_x, pady=padding_y)
    entry_host.insert(0, "localhost")

    ttk.Label(config_window, text="Usuario:").grid(column=0, row=1, sticky=tk.W, padx=padding_x, pady=padding_y)
    entry_usuario = ttk.Entry(config_window, width=30)
    entry_usuario.grid(column=1, row=1, padx=padding_x, pady=padding_y)
    entry_usuario.insert(0, "root")

    ttk.Label(config_window, text="Contraseña:").grid(column=0, row=2, sticky=tk.W, padx=padding_x, pady=padding_y)
    entry_password = ttk.Entry(config_window, width=30, show="*")
    entry_password.grid(column=1, row=2, padx=padding_x, pady=padding_y)

    ttk.Label(config_window, text="Base de datos:").grid(column=0, row=3, sticky=tk.W, padx=padding_x, pady=padding_y)
    entry_base_datos = ttk.Entry(config_window, width=30)
    entry_base_datos.grid(column=1, row=3, padx=padding_x, pady=padding_y)
    entry_base_datos.insert(0, "archivos_excel")

    # Botón para guardar
    ttk.Button(config_window, text="Guardar configuración", command=guardar_configuracion).grid(column=0, row=4, columnspan=2, pady=20)

# Función para procesar el archivo Excel y convertirlo en datos de MySQL
def procesar_excel():
    archivo_excel = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo_excel:
        return

    nombre_tabla = entry_tabla.get()
    if not nombre_tabla:
        messagebox.showerror("Error", "Por favor, ingrese un nombre para la tabla.")
        return

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=usuario,
            password=password,
            database=bd
        )
        
        if conexion.is_connected():
            cursor = conexion.cursor()
            
            df = pd.read_excel(archivo_excel)
            
            crear_tabla(cursor, nombre_tabla, df.dtypes)
            insertar_datos(cursor, nombre_tabla, df)
            
            conexion.commit()
            messagebox.showinfo("Éxito", f"Datos insertados en la tabla '{nombre_tabla}' exitosamente.")
        
    except Error as e:
        messagebox.showerror("Error", f"Error al conectar a MySQL: {e}")
    
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Función para crear la tabla en MySQL
def crear_tabla(cursor, nombre_tabla, columnas):
    columnas_sql = ["id INT AUTO_INCREMENT PRIMARY KEY"]
    for col, dtype in columnas.items():
        if dtype == 'int64':
            tipo = 'INT'
        elif dtype == 'float64':
            tipo = 'FLOAT'
        elif dtype == 'datetime64[ns]':
            tipo = 'DATETIME'
        else:
            tipo = 'VARCHAR(255)'
        columnas_sql.append(f"{col} {tipo}")
    consulta_sql = f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({', '.join(columnas_sql)});"
    cursor.execute(consulta_sql)

# Función para insertar los datos en MySQL
def insertar_datos(cursor, nombre_tabla, df):
    columnas = ", ".join([f"{col}" for col in df.columns])
    valores = ", ".join(["%s"] * len(df.columns))
    consulta_sql = f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores})"
    for _, fila in df.iterrows():
        cursor.execute(consulta_sql, tuple(fila))

# Ventana principal
root = tk.Tk()
root.title("Conversor de Excel a MySQL")
# root.geometry("400x200")

#esto es para poner la ventana en el medio de la pantalla
def centro_ventana(ventana,ancho,alto):
    x=(ventana.winfo_screenwidth()-ancho)/2
    y=(ventana.winfo_screenheight()-alto)/2
    ventana.geometry(f"{ancho}x{alto}+{int(x)}+{int(y)}")
ancho=400
alto=200

centro_ventana(root,ancho,alto)

# Crear y posicionar los widgets
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Nombre de la tabla:").grid(column=0, row=0, sticky=tk.W, pady=10)
entry_tabla = ttk.Entry(frame, width=30)
entry_tabla.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=10)

# Botones
ttk.Button(frame, text="Seleccionar archivo Excel y convertir", command=procesar_excel).grid(column=0, row=1, columnspan=2, pady=10)
ttk.Button(frame, text="Configuración", command=abrir_configuracion).grid(column=0, row=2, columnspan=2, pady=10)

for child in frame.winfo_children(): 
    child.grid_configure(padx=10)

# Valores por defecto para la conexión
host = "localhost"
usuario = "root"
password = ""
bd = "archivos_excel"

root.mainloop()
