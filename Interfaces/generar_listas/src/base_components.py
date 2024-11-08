# base_components.py
import tkinter as tk
from tkinter import ttk
from typing import Callable
from src.config import Config

class BaseComponent:
    """Clase base para componentes de la interfaz."""
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.widget = None

class ComboBoxGroup(BaseComponent):
    """Componente para grupo de comboboxes."""
    def __init__(self, parent: tk.Widget, label: str, width: int = 30, state: str = "readonly"):
        super().__init__(parent)
        self.frame = ttk.Frame(parent)
        self.label = ttk.Label(self.frame, text=f"{label}:", 
                             style='CardBody.TLabel', width=10)
        self.combobox = ttk.Combobox(self.frame, state=state, width=width)
        
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        self.label.pack(side='left', padx=(0, 10))
        self.combobox.pack(side='left', padx=(0, 20))
        
    def bind(self, event: str, callback: Callable):
        self.combobox.bind(event, callback)
        
    def set(self, value: str):
        self.combobox.set(value)
        
    def get(self) -> str:
        return self.combobox.get()

class CustomTable(BaseComponent):
    """Componente personalizado para tabla de datos."""
    def __init__(self, parent: tk.Widget, columns: tuple):
        super().__init__(parent)
        self.frame = ttk.Frame(parent)
        
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", 
                                     command=self.tree.yview)
        
        for col in columns:
            self.tree.heading(col, text=col)
            
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        self.tree.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')
        
    def insert(self, values: tuple):
        self.tree.insert("", "end", values=values)
        
    def clear(self):
        self.tree.delete(*self.tree.get_children())

class Footer(BaseComponent):
    """Componente para el pie de página."""
    def __init__(self, parent: tk.Widget, on_return: Callable, on_close: Callable):
        super().__init__(parent)
        self.frame = ttk.Frame(parent)
        
        self.copyright = ttk.Label(
            self.frame, 
            text="© 2024 Sistema de Gestión de Documentos",
            font=Config.UI_CONFIG["fonts"]["footer"]
        )
        
        self.button_frame = ttk.Frame(self.frame)
        self.return_btn = ttk.Button(
            self.button_frame,
            text=Config.UI_CONFIG["buttons"]["return"]["text"],
            style='Footer.TButton',
            command=on_return
        )
        
        self.close_btn = ttk.Button(
            self.button_frame,
            text=Config.UI_CONFIG["buttons"]["close"]["text"],
            style='Footer.TButton',
            command=on_close
        )
        
    def pack(self):
        self.frame.pack(side='bottom', fill='x', pady=(20, 0))
        self.copyright.pack(side='left')
        self.button_frame.pack(side='right')
        self.return_btn.pack(side='right', padx=(0, 10))
        self.close_btn.pack(side='right', padx=(0, 10))