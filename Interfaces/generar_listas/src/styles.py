# styles.py
from tkinter import ttk
from src.config import Config

class StyleManager:
    """Administrador de estilos para la aplicación."""
    @staticmethod
    def configure_styles():
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background=Config.UI_CONFIG["colors"]["primary"])
        style.configure('TLabel', background=Config.UI_CONFIG["colors"]["primary"], foreground=Config.UI_CONFIG["colors"]["secondary"], font=('Segoe UI', 12))
        style.configure('TButton', font=('Segoe UI', 10))
        
        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), foreground=Config.UI_CONFIG["colors"]["secondary"])
        
        style.configure('Card.TFrame', background='#FFFFFF', relief='flat')
        style.configure('CardTitle.TLabel', background='#FFFFFF', foreground=Config.UI_CONFIG["colors"]["secondary"], font=('Segoe UI', 16, 'bold'))
        style.configure('CardBody.TLabel', background='#FFFFFF', foreground='#4A5568', font=('Segoe UI', 10))
        style.configure('Card.TButton', background=Config.UI_CONFIG["colors"]["accent"], foreground='white', font=('Segoe UI', 10, 'bold'))
        style.map('Card.TButton', background=[('active', '#3182CE')])

        style.configure('Footer.TButton', background='#E2E8F0', foreground='#4A5568', font=('Segoe UI', 9))
        style.map('Footer.TButton', background=[('active', '#CBD5E0')])
            
    @staticmethod
    def apply_widget_styles(widget: ttk.Widget, style_name: str):
        """Aplica un estilo específico a un widget."""
        if isinstance(widget, ttk.Widget):
            widget.configure(style=style_name)