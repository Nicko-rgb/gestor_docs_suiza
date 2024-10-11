import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import mysql.connector
from mysql.connector import Error
import sys
import os

# Obtener el directorio actual (donde está excel_sql_id.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Obtener el directorio del proyecto (el directorio superior)
parent_dir = os.path.dirname(current_dir)
# Agregar el directorio del proyecto a sys.path
sys.path.append(parent_dir)
# Agregar el directorio de Interfaces a sys.path
interfaces_path = os.path.join(parent_dir, 'Interfaces')
sys.path.append(interfaces_path)

#print(sys.path)  # Para verificar que las rutas se han añadido correctamente

class ExcelToMySQLConverter:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "archivos_excel"
        self.root = None
        self.entry_table = None

    def create_main_window(self):
        self.root = tk.Tk()
        self.root.title("Excel to MySQL Converter")
        self.root.overrideredirect(True)
        width, height = 1000, 800

        self.center_window(self.root, width, height)
        def volver():
            from Inicio.menu_principal import abrir_menu_principal
            self.root.destroy()
            abrir_menu_principal()

        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Table name:").grid(column=0, row=0, sticky=tk.W, pady=10)
        
        self.entry_table = ttk.Entry(frame, width=30)
        self.entry_table.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=10)
        ttk.Label(frame, text="Excel to MySQL Converter", font=('Arial',14,'bold')).place(x=10,y=10)
        ttk.Button(frame, text="Select Excel file and convert", command=self.process_excel).grid(column=0, row=1, columnspan=2, pady=10)
        ttk.Button(frame, text="Configuration", command=self.open_configuration).grid(column=0, row=2, columnspan=2, pady=10)
        ttk.Button(frame, text="Volver", command=volver).grid(column=0, row=3, columnspan=2, pady=10)

        for child in frame.winfo_children(): 
            child.grid_configure(padx=10)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def open_configuration(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Connection Configuration")
        config_window.geometry("320x220")

        padding = 10

        ttk.Label(config_window, text="Host:").grid(column=0, row=0, sticky=tk.W, padx=padding, pady=padding)
        entry_host = ttk.Entry(config_window, width=30)
        entry_host.grid(column=1, row=0, padx=padding, pady=padding)
        entry_host.insert(0, self.host)

        ttk.Label(config_window, text="User:").grid(column=0, row=1, sticky=tk.W, padx=padding, pady=padding)
        entry_user = ttk.Entry(config_window, width=30)
        entry_user.grid(column=1, row=1, padx=padding, pady=padding)
        entry_user.insert(0, self.user)

        ttk.Label(config_window, text="Password:").grid(column=0, row=2, sticky=tk.W, padx=padding, pady=padding)
        entry_password = ttk.Entry(config_window, width=30, show="*")
        entry_password.grid(column=1, row=2, padx=padding, pady=padding)

        ttk.Label(config_window, text="Database:").grid(column=0, row=3, sticky=tk.W, padx=padding, pady=padding)
        entry_database = ttk.Entry(config_window, width=30)
        entry_database.grid(column=1, row=3, padx=padding, pady=padding)
        entry_database.insert(0, self.database)

        ttk.Button(config_window, text="Save configuration", 
                   command=lambda: self.save_configuration(entry_host.get(), entry_user.get(), 
                                                           entry_password.get(), entry_database.get(), 
                                                           config_window)).grid(column=0, row=4, columnspan=2, pady=20)

    def save_configuration(self, host, user, password, database, window):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        window.destroy()

    def process_excel(self):
        excel_file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not excel_file:
            return

        table_name = self.entry_table.get()
        if not table_name:
            messagebox.showerror("Error", "Please enter a table name.")
            return

        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                
                df = pd.read_excel(excel_file)
                
                self.create_table(cursor, table_name, df.dtypes)
                self.insert_data(cursor, table_name, df)
                
                connection.commit()
                messagebox.showinfo("Success", f"Data inserted into table '{table_name}' successfully.")
            
        except Error as e:
            messagebox.showerror("Error", f"Error connecting to MySQL: {e}")
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def create_table(self, cursor, table_name, columns):
        columns_sql = ["id INT AUTO_INCREMENT PRIMARY KEY"]
        for col, dtype in columns.items():
            if dtype == 'int64':
                col_type = 'INT'
            elif dtype == 'float64':
                col_type = 'FLOAT'
            elif dtype == 'datetime64[ns]':
                col_type = 'DATETIME'
            else:
                col_type = 'VARCHAR(255)'
            columns_sql.append(f"`{col}` {col_type}")
        sql_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({', '.join(columns_sql)});"
        cursor.execute(sql_query)

    def insert_data(self, cursor, table_name, df):
        columns = ", ".join([f"`{col}`" for col in df.columns])
        values = ", ".join(["%s"] * len(df.columns))
        sql_query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({values})"
        for _, row in df.iterrows():
            cursor.execute(sql_query, tuple(row))

    def run(self):
        self.create_main_window()
        self.root.mainloop()

if __name__ == "__main__":
    converter = ExcelToMySQLConverter()
    converter.run()
