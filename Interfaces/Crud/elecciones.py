import tkinter as tk
from tkinter import ttk
from Crud.crud_interface import CrudInterface

class Elecciones:
    def __init__(self, master, db_path):
        self.master = master
        self.db_path = db_path
        self._setup_styles()
        self.setup_ui()

    def _setup_styles(self):
        """Configura los estilos de la interfaz."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuración de colores
        self.colors = {
            'bg': '#6f6f6f',
            'fg': '#2D3748',
            'card_bg': '#FFFFFF',
            'button_bg': '#4299E1',
            'button_active': '#3182CE',
            'text_secondary': '#4A5568',
            'header_bg': '#6f6f6f',
            'success': '#48BB78',
            'warning': '#ED8936',
            'danger': '#F56565'
        }

        # Estilos base
        style.configure('Main.TFrame', background=self.colors['bg'])
        style.configure('Card.TFrame', background=self.colors['card_bg'])
        
        # Estilo para botones
        style.configure('Action.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['button_bg'],
                       foreground='white',
                       padding=(10, 5))
        
        style.map('Action.TButton',
                 background=[('active', self.colors['button_active'])])
        
        style.configure('Danger.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['danger'],
                       foreground='white',
                       padding=(10, 5))

    def setup_ui(self):
        self.master.title("Elección de Edición")
        self.master.geometry("500x400")
        self.master.resizable(False, False)
        
        # Configurar el color de fondo de la ventana principal
        self.master.configure(bg=self.colors['bg'])

        # Ocultar los bordes de la ventana
        self.master.overrideredirect(1)

        # Centrar la ventana en la pantalla
        self.center_window(500, 400)

        # Crear marcos
        self.create_button_frame()
        self.create_middle_buttons()

    def center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def create_button_frame(self):
        button_frame = ttk.Frame(self.master, style='Main.TFrame')
        button_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)

        back_button = ttk.Button(
            button_frame, 
            text="Volver", 
            command=self.master.destroy,
            style='Action.TButton'
        )
        back_button.pack(side=tk.LEFT, padx=10)

        close_button = ttk.Button(
            button_frame, 
            text="Cerrar", 
            command=self.master.destroy,
            style='Danger.TButton'
        )
        close_button.pack(side=tk.RIGHT, padx=10)

    def open_student_edit(self):
        student_window = tk.Toplevel(self.master)
        student_window.configure(bg=self.colors['bg'])
        CrudInterface(student_window, self.db_path)

    def create_middle_buttons(self):
        middle_frame = ttk.Frame(self.master, style='Main.TFrame')
        middle_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        button1 = ttk.Button(
            middle_frame, 
            text="Editar Estudiantes", 
            command=self.open_student_edit,
            style='Action.TButton'
        )
        button1.pack(pady=120)

    def open_window(self, title):
        new_window = tk.Toplevel(self.master)
        new_window.title(title)
        new_window.geometry("400x300")
        new_window.configure(bg=self.colors['bg'])
        new_window.transient(self.master)
        new_window.grab_set()
        
        label = ttk.Label(
            new_window, 
            text=title,
            style='Title.TLabel'
        )
        label.pack(pady=20)