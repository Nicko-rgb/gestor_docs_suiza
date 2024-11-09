import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from .ui_config import UI_CONFIG

class DocumentGeneratorUI:
    def __init__(self, document_generator, parent=None):
        self.document_generator = document_generator
        # Si tiene padre, crear Toplevel, si no, crear Tk
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title(UI_CONFIG["window"]["title"])
        self._center_window(self.root, UI_CONFIG["window"]["width"], UI_CONFIG["window"]["height"])
        
        # Eliminar overrideredirect para permitir decoración de ventana
        self.root.overrideredirect(1)  # Comentado
        
        # Configurar ventana
        if isinstance(self.root, tk.Toplevel):
            self.root.transient(parent)  # Hacer la ventana dependiente del padre
            self.root.grab_set()  # Hacer la ventana modal
        
        self._configure_styles()
        self.input_fields = {}
        self.on_close_callback = None

    def _configure_styles(self):
        style = ttk.Style(self.root)  # Vincular el estilo a esta ventana específica
        style.theme_use('clam')

        colors = UI_CONFIG["colors"]

        # Configuraciones base con background explícito
        style.configure('.', background=colors["primary"])
        style.configure('TFrame', background=colors["primary"])
        style.configure('TLabel', 
                       background=colors["primary"], 
                       foreground=colors["secondary"], 
                       font=('Segoe UI', 12))
        style.configure('TEntry', 
                       fieldbackground='white',
                       background='white',
                       font=('Segoe UI', 10))
        style.configure('TButton', 
                       font=('Segoe UI', 10),
                       background=colors["accent"])

        # Estilos específicos mejorados
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'), 
                       foreground=colors["secondary"],
                       background=colors["primary"])

        style.configure('Card.TFrame', 
                       background='white', 
                       relief='flat',
                       borderwidth=0)
        
        style.configure('CardTitle.TLabel', 
                       background='white', 
                       foreground=colors["secondary"], 
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('CardBody.TLabel', 
                       background='white', 
                       foreground='#4A5568', 
                       font=('Segoe UI', 10))
        
        style.configure('Card.TButton', 
                       background=colors["accent"], 
                       foreground='white', 
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))
        
        # Mapeos de estados mejorados
        style.map('Card.TButton', 
                 background=[('active', '#3182CE'), ('pressed', '#2C5282')],
                 relief=[('pressed', 'sunken')])

        style.configure('Footer.TButton', 
                       background='#E2E8F0', 
                       foreground='#4A5568', 
                       font=('Segoe UI', 9))
        
        style.map('Footer.TButton', 
                 background=[('active', '#CBD5E0'), ('pressed', '#A0AEC0')])

    def create_interface(self):
        # Configurar el color de fondo de la ventana principal
        self.root.configure(background=UI_CONFIG["colors"]["primary"])
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)

        # Título con fondo correcto
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 40))
        ttk.Label(title_frame, 
                 text="Generador de cartas de presentación", 
                 style='Title.TLabel').pack()

        # Card con borde y sombra
        card_frame = ttk.Frame(main_frame, style='Card.TFrame')
        card_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Contenedor para los campos
        fields_container = ttk.Frame(card_frame)
        fields_container.pack(fill='both', expand=True, padx=20, pady=20)

        for field in UI_CONFIG["fields"]:
            field_frame = ttk.Frame(fields_container)
            field_frame.pack(fill='x', pady=5)

            ttk.Label(field_frame, 
                     text=field["label"], 
                     style='CardBody.TLabel', 
                     width=20, 
                     anchor='e').pack(side='left', padx=(0, 10))
            
            entry = ttk.Entry(field_frame, 
                            width=30, 
                            font=('Segoe UI', 10))
            entry.pack(side='left', expand=True, fill='x')
            self.input_fields[field["var_name"]] = entry

        # Frame para botones centrados
        button_frame = ttk.Frame(card_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, 
                  text=UI_CONFIG["buttons"]["generate"]["text"], 
                  style='Card.TButton',
                  command=self._generate_document).pack(padx=10)

        # Footer mejorado
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side='bottom', fill='x', pady=(20, 0))

        ttk.Label(footer_frame, 
                 text="© 2024 Sistema de Gestión de documentos",
                 font=('Segoe UI', 8)).pack(side='left')

        ttk.Button(footer_frame, 
                  text=UI_CONFIG["buttons"]["back"]["text"],
                  style='Footer.TButton',
                  command=self.go_back).pack(side='right', padx=10)

    def _center_window(self, window, width, height):
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def _generate_document(self):
        data = {field["var_name"]: self.input_fields[field["var_name"]].get() 
                for field in UI_CONFIG["fields"]}
        self.document_generator.generate_document(data)

    def get_file_name(self):
        return simpledialog.askstring("Guardar como", 
                                    "Introduce el nombre del archivo (sin extensión):")

    def clear_fields(self):
        for field in self.input_fields.values():
            field.delete(0, tk.END)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def show_success_message(self, message):
        messagebox.showinfo("Éxito", message)

    def set_on_close(self, callback):
        self.on_close_callback = callback

    def go_back(self):
        self.root.destroy()
        if self.on_close_callback:
            self.on_close_callback()

    def run(self):
        self.create_interface()
        if isinstance(self.root, tk.Toplevel):
            # Si es una ventana secundaria
            self.root.transient(self.root.master)
            self.root.grab_set()
            self.root.focus_set()
            self.root.wait_window()
        else:
            # Si es la ventana principal
            self.root.mainloop()