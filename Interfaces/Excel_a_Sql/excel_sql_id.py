import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

class ExcelToMySQLConverter:
    def __init__(self, parent=None):
        self.parent = parent
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "archivos_excel"
        self.root = None
        self.entry_table = None
        self.config_window = None
        self.on_close_callback = None

    def create_main_window(self):
        if self.parent:
            self.root = tk.Toplevel(self.parent)
        else:
            self.root = tk.Tk()
        
        self.root.title("Excel to MySQL Converter")
        self.configure_styles()
        
        # Quitar la barra de arriba
        self.root.overrideredirect(1)
        
        width, height = 600, 400
        self.center_window(self.root, width, height)

        main_frame = ttk.Frame(self.root, style='Main.TFrame', padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Excel to MySQL Converter", style='Title.TLabel').pack(pady=(0, 30))

        input_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="20")
        input_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(input_frame, text="Table name:", style='CardBody.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.entry_table = ttk.Entry(input_frame, width=30, font=('Segoe UI', 10))
        self.entry_table.pack(fill=tk.X, pady=(0, 20))

        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Select Excel file and convert", style='Card.TButton',
                   command=self.process_excel).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Configuration", style='Card.TButton',
                   command=self.open_configuration).pack(side=tk.LEFT)

        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))

        ttk.Label(footer_frame, text="© 2024 Excel to MySQL Converter", style='Footer.TLabel').pack(side=tk.LEFT)
        
        # Add the Back button
        ttk.Button(footer_frame, text="Volver", style='Footer.TButton', command=self.go_back).pack(side=tk.RIGHT, padx=(0, 10))
        ttk.Button(footer_frame, text="Cerrar", style='Footer.TButton', command=self.root.destroy).pack(side=tk.RIGHT)

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Definir colores
        bg_color = '#F0F4F8'
        fg_color = '#2D3748'
        card_bg = '#FFFFFF'
        button_bg = '#4299E1'
        button_active = '#3182CE'

        # Configuraciones generales
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 12))
        style.configure('TButton', font=('Segoe UI', 10))
        
        # Estilos específicos
        style.configure('Main.TFrame', background=bg_color)
        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), foreground=fg_color, background=bg_color)
        style.configure('Card.TFrame', background=card_bg, relief='flat')
        style.configure('CardBody.TLabel', background=card_bg, foreground=fg_color, font=('Segoe UI', 10))
        style.configure('Card.TButton', background=button_bg, foreground='white', font=('Segoe UI', 10, 'bold'))
        style.map('Card.TButton', background=[('active', button_active)])
        style.configure('Footer.TLabel', font=('Segoe UI', 8), background=bg_color)
        style.configure('Footer.TButton', background='#E2E8F0', foreground=fg_color, font=('Segoe UI', 9))
        style.map('Footer.TButton', background=[('active', '#CBD5E0')])
        
        # Configurar el estilo para el Entry
        style.configure('TEntry', font=('Segoe UI', 10))  # Mover esta línea aquí


    def open_configuration(self):
        self.config_window = tk.Toplevel(self.root)
        self.config_window.title("Connection Configuration")
        self.config_window.geometry("400x300")
        self.center_window(self.config_window, 400, 300)

        config_frame = ttk.Frame(self.config_window, style='Card.TFrame', padding="20")
        config_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(config_frame, text="Database Configuration", style='Title.TLabel').pack(pady=(0, 20))

        entries = {}
        for field in ['Host', 'User', 'Password', 'Database']:
            ttk.Label(config_frame, text=f"{field}:", style='CardBody.TLabel').pack(anchor=tk.W, pady=(0, 5))
            entry = ttk.Entry(config_frame, width=30, font=('Segoe UI', 10))
            entry.pack(fill=tk.X, pady=(0, 10))
            entries[field.lower()] = entry

        entries['host'].insert(0, self.host)
        entries['user'].insert(0, self.user)
        entries['database'].insert(0, self.database)

        ttk.Button(config_frame, text="Save configuration", style='Card.TButton',
                   command=lambda: self.save_configuration(entries)).pack(pady=(20, 0))

    def save_configuration(self, entries):
        self.host = entries['host'].get()
        self.user = entries['user'].get()
        self.password = entries['password'].get()
        self.database = entries['database'].get()
        self.config_window.destroy()
        messagebox.showinfo("Success", "Configuration saved successfully.")

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

    def go_back(self):
        self.root.destroy()
        if self.on_close_callback:
            self.on_close_callback()

    def set_on_close(self, callback):
        self.on_close_callback = callback
        
    def center_window(self, window, width, height):
        # Asegúrate de que este método esté definido
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')
        
    def run(self):
        self.create_main_window()
        self.root.after(100, self.root.deiconify)  # Pequeño retraso antes de mostrar la ventana
        if not self.parent:
            self.root.mainloop()

if __name__ == "__main__":
    converter = ExcelToMySQLConverter()
    converter.run()