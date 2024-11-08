import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from src.ui_config import UI_CONFIG

class DocumentGeneratorUI:
    def __init__(self, document_generator):
        self.document_generator = document_generator
        self.root = tk.Tk()  # Use tk.Tk() instead of tk.Toplevel()
        self.root.title(UI_CONFIG["window"]["title"])
        self._center_window(self.root, UI_CONFIG["window"]["width"], UI_CONFIG["window"]["height"])
        self._configure_styles()
        self.input_fields = {}

    def create_interface(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)

        ttk.Label(main_frame, text="Generador de cartas de presentación", style='Title.TLabel').pack(pady=(0, 40))

        card_frame = ttk.Frame(main_frame, style='Card.TFrame')
        card_frame.pack(fill='both', expand=True, padx=20, pady=20)

        self.root.overrideredirect(1)  # Quitar la barra de arriba
        
        for field in UI_CONFIG["fields"]:
            field_frame = ttk.Frame(card_frame)
            field_frame.pack(fill='x', pady=5)

            ttk.Label(field_frame, text=field["label"], style='CardBody.TLabel', width=20, anchor='e').pack(side='left', padx=(0, 10))
            entry = ttk.Entry(field_frame, width=30, font=('Arial', 12))
            entry.pack(side='left', expand=True, fill='x')
            self.input_fields[field["var_name"]] = entry

        button_frame = ttk.Frame(card_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text=UI_CONFIG["buttons"]["generate"]["text"], style='Card.TButton', 
                   command=self._generate_document).pack(side='left', padx=10)

        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side='bottom', fill='x', pady=(20, 0))

        ttk.Label(footer_frame, text="© 2024 Sistema de Gestión de documentos", 
                  font=('Segoe UI', 8)).pack(side='left')

        ttk.Button(footer_frame, text=UI_CONFIG["buttons"]["back"]["text"], 
                   style='Footer.TButton', 
                   command=self.go_back).pack(side='right', padx=(0, 10))

        ttk.Button(footer_frame, text="Cerrar", style='Footer.TButton', 
                   command=self.root.destroy).pack(side='right')
        self.set_on_close(self.go_back)
        
    def _generate_document(self):
        data = {field["var_name"]: self.input_fields[field["var_name"]].get() for field in UI_CONFIG["fields"]}
        self.document_generator.generate_document(data)

    def get_file_name(self):
        return simpledialog.askstring("Guardar como", "Introduce el nombre del archivo (sin extensión):")

    def clear_fields(self):
        for field in self.input_fields.values():
            field.delete(0, tk.END)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)
        
    def show_success_message(self, message):
        messagebox.showinfo("Éxito", message)
        
    def set_on_close(self, callback):
        self.on_close_callback = callback

    def _center_window(self, window, width, height):
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background=UI_CONFIG["colors"]["primary"])
        style.configure('TLabel', background=UI_CONFIG["colors"]["primary"], foreground=UI_CONFIG["colors"]["secondary"], font=('Segoe UI', 12))
        style.configure('TButton', font=('Segoe UI', 10))

        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), foreground=UI_CONFIG["colors"]["secondary"])

        style.configure('Card.TFrame', background='#FFFFFF', relief='flat')
        style.configure('CardTitle.TLabel', background='#FFFFFF', foreground=UI_CONFIG["colors"]["secondary"], font=('Segoe UI', 16, 'bold'))
        style.configure('CardBody.TLabel', background='#FFFFFF', foreground='#4A5568', font=('Segoe UI', 10))
        style.configure('Card.TButton', background=UI_CONFIG["colors"]["accent"], foreground='white', font=('Segoe UI', 10, 'bold'))
        style.map('Card.TButton', background=[('active', '#3182CE')])

        style.configure('Footer.TButton', background='#E2E8F0', foreground='#4A5568', font=('Segoe UI', 9))
        style.map('Footer.TButton', background=[('active', '#CBD5E0')])

    def run(self):
        self.create_interface()
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        self.document_generator.set_on_close(self.go_back)
        self.root.grab_set()  # Hace que esta ventana sea modal
        self.root.wait_window()  # Espera hasta que la ventana se cierre

    def go_back(self):
        self.root.destroy()
        if self.on_close_callback:
            self.on_close_callback()