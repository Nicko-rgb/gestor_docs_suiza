# Interfaces/config/config_manager.py

import json
import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox
from typing import Dict, Optional
from Crud.crud_interface import CrudInterface
from Crud.elecciones import Elecciones

class ConfigManager:
    def __init__(self, parent: Optional[tk.Tk] = None):
        self.parent = parent
        self.window: Optional[tk.Toplevel] = None
        self.config_file = "config.json"
        self.default_config = {
            "docs_path": "",
            "output_path": ""
        }
        self.load_config()

    def load_config(self) -> Dict:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = self.default_config.copy()
                self.save_config()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la configuración: {str(e)}")
            self.config = self.default_config.copy()
        return self.config

    def save_config(self) -> None:
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la configuración: {str(e)}")

    def browse_directory(self, entry: ttk.Entry) -> None:
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)

    def _setup_styles(self) -> None:
        """Configura los estilos de la interfaz."""
        style = ttk.Style()
        
        # Configuración de colores
        colors = {
            'bg': '#F0F4F8',
            'fg': '#2D3748',
            'card_bg': '#FFFFFF',
            'button_bg': '#4299E1',
            'button_active': '#3182CE',
            'text_secondary': '#4A5568'
        }

        # Estilos específicos para la ventana de configuración
        styles = {
            'Config.TFrame': {
                'background': colors['bg']
            },
            'ConfigCard.TFrame': {
                'background': colors['card_bg']
            },
            'Config.TLabel': {
                'background': colors['card_bg'],
                'foreground': colors['fg'],
                'font': ('Segoe UI', 10)
            },
            'ConfigTitle.TLabel': {
                'background': colors['bg'],
                'foreground': colors['fg'],
                'font': ('Segoe UI', 16, 'bold')
            },
            'Config.TButton': {
                'font': ('Segoe UI', 10)
            },
            'ConfigBrowse.TButton': {
                'font': ('Segoe UI', 10)
            },
            'ConfigAction.TButton': {
                'font': ('Segoe UI', 10)
            }
        }

        for style_name, config in styles.items():
            style.configure(style_name, **config)

    def show_config_window(self) -> None:
        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            return

        # Configuración de la ventana
        self.window = tk.Toplevel(self.parent)
        self.window.title("Configuración")
        
        # Configurar dimensiones y posición
        width, height = 450, 250  # Ventana más pequeña
        x = (self.window.winfo_screenwidth() - width) // 2
        y = (self.window.winfo_screenheight() - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Hacer la ventana modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Configurar estilos
        self._setup_styles()

        # Frame principal con padding reducido
        main_frame = ttk.Frame(self.window, style='Config.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título de la ventana
        title_frame = ttk.Frame(main_frame, style='Config.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(title_frame, text="Configuración", 
                 style='ConfigTitle.TLabel').pack(side=tk.LEFT)

        # Tarjeta de configuración
        card_frame = ttk.Frame(main_frame, style='ConfigCard.TFrame')
        card_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Frame para el contenido con padding reducido
        content_frame = ttk.Frame(card_frame, style='ConfigCard.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Diccionario para almacenar las entradas
        entries = {}

        # Crear campos de configuración
        paths = [
            ("Ruta de Generador de Carta:", "docs_path"),
            ("Ruta de Generador de Lista:", "output_path")
        ]

        for i, (label_text, config_key) in enumerate(paths):
            # Frame para cada fila
            row_frame = ttk.Frame(content_frame, style='ConfigCard.TFrame')
            row_frame.pack(fill=tk.X, pady=5)  # Reducido el padding vertical
            
            # Label
            label = ttk.Label(row_frame, text=label_text, style='Config.TLabel')
            label.pack(side=tk.LEFT)

            # Frame para entrada y botón
            input_frame = ttk.Frame(row_frame, style='ConfigCard.TFrame')
            input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))  # Reducido el padding

            # Entry
            entry = ttk.Entry(input_frame, font=('Segoe UI', 9))  # Fuente más pequeña
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            if self.config[config_key]:
                entry.insert(0, self.config[config_key])
            entries[config_key] = entry

            # Botón Browse
            browse_btn = ttk.Button(
                input_frame, 
                text="...", 
                style='ConfigBrowse.TButton',
                width=2,  # Botón más pequeño
                command=lambda e=entry: self.browse_directory(e)
            )
            browse_btn.pack(side=tk.LEFT, padx=(3, 0))  # Reducido el padding

        # Frame para botones de acción
        button_frame = ttk.Frame(content_frame, style='ConfigCard.TFrame')
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))  # Reducido el padding

        # Botones de edición
        def open_student_edit():
            student_window = tk.Toplevel(self.window)
            CrudInterface(student_window, "documentos_base_de_datos.db")
        
        def open_chosse():
            chosse_window = tk.Toplevel(self.window)
            Elecciones(chosse_window, "documentos_base_de_datos.db")

        def save_and_close():
            for key, entry in entries.items():
                self.config[key] = entry.get()
            self.save_config()
            self.window.destroy()
            self.window = None

        # Botones de acción
        ttk.Button(
            button_frame, 
            text="Cancelar",
            style='ConfigAction.TButton',
            command=lambda: self.window.destroy()
        ).pack(side=tk.RIGHT, padx=(3, 0))

        ttk.Button(
            button_frame, 
            text="Guardar",
            style='ConfigAction.TButton',
            command=save_and_close
        ).pack(side=tk.RIGHT)

        # Botones de edición
        try:
            ttk.Button(
                button_frame, 
                text="Edición de Estudiantes",
                style='ConfigAction.TButton',
                command=open_student_edit
            ).pack(side=tk.LEFT, padx=(1, 0))
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la ventana de edición de estudiantes: {str(e)}")

        # Manejar cierre de ventana
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())
        self.window.bind("<Destroy>", self._on_destroy)
    

    def _on_destroy(self, event=None):
        self.window = None

    def get_config(self, key: str) -> str:
        return self.config.get(key, self.default_config.get(key, ""))