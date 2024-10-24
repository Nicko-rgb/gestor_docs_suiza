import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from typing import Callable, Optional, Dict, Type
from pathlib import Path
import logging
from PIL import Image, ImageTk

class MenuPrincipal:
    def __init__(self):
        """Inicializa el menú principal de la aplicación."""
        self.root: Optional[tk.Tk] = None
        self.modules: Dict[str, Type] = {}
        self.current_dir: Path = None
        self.interface_dir: Path = None
        self.excel_sql_path: Path = None
        self.config_manager = None
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self._setup_environment()
        self._import_modules()
    
    def _setup_environment(self) -> None:
        try:
            # Modificar para usar las rutas correctamente
            self.current_dir = Path(__file__).resolve().parent  # Inicio/
            self.interface_dir = self.current_dir.parent        # Raíz del proyecto
            
            # Agregar la raíz del proyecto al sys.path
            if str(self.interface_dir) not in sys.path:
                sys.path.insert(0, str(self.interface_dir))
            
            # Ahora importar ConfigManager
            from config.config_manager import ConfigManager
            self.config_manager = ConfigManager()
            
            # Cargar configuración
            config = self.config_manager.load_config()
            
            # Establecer ruta de Excel_a_Sql
            excel_sql_path = config.get('excel_sql_path')
            self.excel_sql_path = (
                Path(excel_sql_path) if excel_sql_path
                else self.interface_dir / 'Excel_a_Sql'
            )
            
            # Definir y verificar rutas requeridas
            required_paths = [
                self.interface_dir,
                self.excel_sql_path,
                self.interface_dir / 'Generador_Docs'
            ]
            
            self._add_paths_to_syspath(required_paths)
            
            self.logger.info("Configuración del entorno completada exitosamente")
            
        except Exception as e:
            error_msg = f"Error al configurar el entorno: {str(e)}"
            self.logger.error(error_msg)
            self._show_error("Error de configuración", error_msg)
            sys.exit(1)

    def _add_paths_to_syspath(self, paths: list[Path]) -> None:
        """
        Agrega las rutas proporcionadas al sys.path si no existen.
        Args:
            paths: Lista de rutas (Path objects) a agregar
        """
        for path in paths:
            path_str = str(path.resolve())
            if path_str not in sys.path:
                sys.path.append(path_str)

    def _import_modules(self) -> None:
        """Importa los módulos necesarios para la aplicación."""
        try:
            # Intentar importar los módulos necesarios
            modules_to_import = {
                'document_generator': ('Generador_Docs.generar_docs', 'DocumentGenerator'),
                'attendance_generator': ('Generador_Docs.generador_asis_mejo', 'GeneradorAsistencia'),
                'excel_converter': ('Excel_a_Sql.excel_sql_id', 'ExcelToMySQLConverter')
            }
            
            for module_key, (module_path, class_name) in modules_to_import.items():
                try:
                    module = __import__(module_path, fromlist=[class_name])
                    self.modules[module_key] = getattr(module, class_name)
                except ImportError as e:
                    self.logger.warning(f"No se pudo importar {module_path}: {str(e)}")
                    continue
                
        except Exception as e:
            error_msg = f"Error al importar módulos: {str(e)}\nPaths: {sys.path}"
            self.logger.error(error_msg)
            self._show_error("Error de importación", error_msg)
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
        """Abre un módulo específico de la aplicación."""
        try:
            if module_key in self.modules:
                self.root.withdraw()
                module = self.modules[module_key](self.root)
                module.set_on_close(self._on_module_close)
                module.run()
            else:
                self._show_error("Error", f"Módulo {module_key} no disponible")
        except Exception as e:
            error_msg = f"Error al abrir {module_key}: {str(e)}"
            self.logger.error(error_msg)
            self._show_error("Error al abrir módulo", error_msg)
            self.root.deiconify()

    def _on_module_close(self) -> None:
        """Maneja el cierre de un módulo."""
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
    
        # Crear tarjetas
        cards_config = [
            {
                'title': "Generar Carta de Presentación",
                'description': "Crea cartas de presentación, con todos los datos necesarios.",
                'command': lambda: self._open_module('document_generator'),
                'row': 0, 'column': 0, 'width': 300, 'height': 150
            },
            {
                'title': "Conversor Excel a SQL",
                'description': "Convierte tus hojas de cálculo a bases de datos SQL con facilidad.",
                'command': lambda: self._open_module('excel_converter'),
                'row': 0, 'column': 1, 'width': 300, 'height': 150
            },
            {
                'title': "Generador de Lista",
                'description': "Convierte los datos de la DB a listas de Asistencias según los Ciclos",
                'command': lambda: self._open_module('attendance_generator'),
                'row': 1, 'column': 0, 'width': 650, 'height': 150, 'columnspan': 2
            }
        ]
    
        for card in cards_config:
            self._create_card(cards_frame, **card)
    
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
    
        ttk.Label(footer_frame,
                 text="© 2024 Sistema de Gestión de documentos",
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
            error_msg = f"Error al iniciar la aplicación: {str(e)}"
            self.logger.error(error_msg)
            self._show_error("Error fatal", error_msg)
            sys.exit(1)

if __name__ == "__main__":
    app = MenuPrincipal()
    app.run()