# menu_principal.py
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from typing import Callable, Optional
from config_manager import ConfigManager
from PIL import Image, ImageTk
from config_manager import ConfigManager

class MenuPrincipal:
    def __init__(self):
        self.root: Optional[tk.Tk] = None
        self.modules = {}
        self.config_manager = ConfigManager()
        self._setup_paths()
        self._import_modules()
        
    def _setup_paths(self) -> None:
        """Configura las rutas necesarias para los módulos."""
        try:
            self.current_dir = os.path.dirname(os.path.abspath(__file__))
            self.parent_dir = os.path.dirname(self.current_dir)
            
            # Usar las rutas desde la configuración
            config = self.config_manager.load_config()
            self.excel_sql_path = config.get('excel_sql_path') or os.path.join(self.parent_dir, 'Excel_a_Sql')
            
            # Añadir rutas al path de Python
            for path in [self.parent_dir, self.excel_sql_path]:
                if path and path not in sys.path:
                    sys.path.append(path)
        except Exception as e:
            self._show_error("Error de configuración", f"Error al configurar rutas: {str(e)}")
            sys.exit(1)

    def _import_modules(self) -> None:
        """Importa los módulos necesarios para la aplicación."""
        try:
            from Generador_Docs.generador_asis_mejo import GeneradorAsistencia
            from Generador_Docs.generar_docs import DocumentGenerator
            from Excel_a_Sql.excel_sql_id import ExcelToMySQLConverter
    
            self.modules = {
                'document_generator': DocumentGenerator,
                'excel_converter': ExcelToMySQLConverter,
                'attendance_generator': GeneradorAsistencia
            }
        except ImportError as e:
            self._show_error("Error de importación", 
                            f"Error al importar módulos: {str(e)}\nPaths: {sys.path}")
            sys.exit(1)

    def _setup_styles(self) -> None:
        """Configura los estilos de la interfaz."""
        style = ttk.Style()
        style.theme_use('clam')

        # Configuración de colores
        colors = {
            'bg': '#F0F4F8',
            'fg': '#2D3748',
            'card_bg': '#FFFFFF',
            'button_bg': '#4299E1',
            'button_active': '#3182CE',
            'text_secondary': '#4A5568'
        }

        # Estilos base
        style.configure('TFrame', background=colors['bg'])
        style.configure('TLabel', background=colors['bg'], foreground=colors['fg'], 
                        font=('Segoe UI', 12))
        style.configure('TButton', font=('Segoe UI', 10))

        # Estilos específicos
        styles = {
            'Title.TLabel': {'font': ('Segoe UI', 24, 'bold'), 'foreground': colors['fg']},
            'Card.TFrame': {'background': colors['card_bg'], 'relief': 'flat'},
            'CardTitle.TLabel': {'background': colors['card_bg'], 'foreground': colors['fg'],
                                'font': ('Segoe UI', 16, 'bold')},
            'CardBody.TLabel': {'background': colors['card_bg'], 'foreground': colors['text_secondary'],
                                'font': ('Segoe UI', 10)},
            'Card.TButton': {'background': colors['button_bg'], 'foreground': 'white',
                            'font': ('Segoe UI', 10, 'bold')},
            'Footer.TButton': {'background': '#E2E8F0', 'foreground': colors['text_secondary'],
                            'font': ('Segoe UI', 9)},
            'Config.TButton': {'background': colors['bg'], 'foreground': colors['fg'],
                            'font': ('Segoe UI', 14)},
        }

        for style_name, config in styles.items():
            style.configure(style_name, **config)

        # Mapeos de estados
        style.map('Card.TButton', background=[('active', colors['button_active'])])
        style.map('Footer.TButton', background=[('active', '#CBD5E0')])
        style.map('Config.TButton', background=[('active', '#E2E8F0')])

    def _create_card(self, parent: ttk.Frame, title: str, description: str, 
                    command: Callable, row: int, column: int, width: int = 200, 
                    height: int = 200, columnspan: int = 1) -> None:
        """Crea una tarjeta en la interfaz."""
        card = ttk.Frame(parent, style='Card.TFrame', padding=(20, 20, 20, 20),
                        width=width, height=height)
        card.grid(row=row, column=column, padx=10, pady=10, sticky='nsew',
                columnspan=columnspan)
        
        ttk.Label(card, text=title, style='CardTitle.TLabel').pack(pady=(0, 10))
        ttk.Label(card, text=description, style='CardBody.TLabel',
                wraplength=width-40).pack(pady=(0, 20))
        ttk.Button(card, text="Abrir", style='Card.TButton',
                command=command).pack()
        
        card.grid_propagate(False)

    def _show_error(self, title: str, message: str) -> None:
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)

    def _open_module(self, module_key: str) -> None:
        try:
            if module_key == 'document_generator':
                self.root.withdraw()
                generator = self.modules[module_key](self.root)
                generator.set_on_close(self._on_module_close)
                generator.run()
            
            elif module_key == 'excel_converter':
                self.root.withdraw()
                converter = self.modules[module_key](self.root)
                converter.set_on_close(self._on_module_close)
                converter.run()
            
            elif module_key == 'attendance_generator':
                self.root.withdraw()
                generator = self.modules[module_key](self.root)
                generator.set_on_close(self._on_module_close)
                generator.run()

        except Exception as e:
            self._show_error("Error al abrir módulo", 
                            f"Error al abrir {module_key}: {str(e)}")
            self.root.deiconify() 

    def _on_module_close(self) -> None:
        self.root.deiconify()
        
    def _setup_main_window(self) -> None:
        """Configura la ventana principal."""
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión Empresarial")
        self.root.overrideredirect(1)
    
        # Configuración de dimensiones y posición
        width, height = 800, 600
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="40 40 40 40")
        main_frame.pack(fill=tk.BOTH, expand=True)
    
        # Título
        ttk.Label(main_frame, text="Panel de Control",
                style='Title.TLabel').pack(pady=(0, 40))
        
        # Botón de configuración
        config_button = ttk.Button(main_frame, 
                                text="⚙", 
                                style='Config.TButton',
                                width=3,
                                command=lambda: self.config_manager.show_config_window())
        config_button.place(x=690, y=10)
    
        # Frame para tarjetas
        cards_frame = ttk.Frame(main_frame)
        cards_frame.pack(fill=tk.BOTH, expand=True)
    
        for i in range(2):
            cards_frame.grid_rowconfigure(i, weight=1)
            cards_frame.grid_columnconfigure(i, weight=1)
    
        # Crear tarjetas con altura reducida
        cards_config = [
            {
                'title': "Generar Carta de Presentación",
                'description': "Crea cartas de presentación, con todos los datos necesarios.",
                'command': lambda: self._open_module('document_generator'),
                'row': 0, 'column': 0, 'width': 300, 'height': 50  # Altura reducida a 100
            },
            {
                'title': "Conversor Excel a SQL",
                'description': "Convierte tus hojas de cálculo a bases de datos SQL con facilidad.",
                'command': lambda: self._open_module('excel_converter'),
                'row': 0, 'column': 1, 'width': 300, 'height': 100  # Altura reducida a 100
            },
            {
                'title': "Generador de Lista",
                'description': "Convierte los datos de la DB a listas de Asistencias según los Ciclos",
                'command': lambda: self._open_module('attendance_generator'),
                'row': 1, 'column': 0, 'width': 650, 'height': 100, 'columnspan': 2  # Altura reducida a 100
            }
        ]
    
        for card in cards_config:
            self._create_card(cards_frame, **card)
    
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
    
        ttk.Label(footer_frame,
                    text="© 2024 Sistema de Gestión Empresarial",
                    font=('Segoe UI', 8)).pack(side=tk.LEFT)
    
        buttons_frame = ttk.Frame(footer_frame)
        buttons_frame.pack(side=tk.RIGHT)
    
        ttk.Button(buttons_frame, text="Cerrar",
                    style='Footer.TButton',
                    command=self.root.quit).pack(side=tk.LEFT)
    def run(self) -> None:
        """Inicia la aplicación."""
        try:
            self._setup_main_window()
            self._setup_styles()
            self.root.mainloop()
        except Exception as e:
            self._show_error("Error fatal",
                            f"Error al iniciar la aplicación: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    app = MenuPrincipal()
    app.run()