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
        self.config_file = os.path.join(Path(__file__).parent, "config.json")
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

    def show_config_window(self) -> None:
        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            return

        self.window = tk.Toplevel(self.parent)
        self.window.title("Configuración")
        self.window.overrideredirect(1)
        width, height = 450, 250
        x = (self.window.winfo_screenwidth() - width) // 2
        y = (self.window.winfo_screenheight() - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        self.window.transient(self.parent)
        self.window.grab_set()
        self._setup_styles()

        main_frame = ttk.Frame(self.window, style='Config.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        title_frame = ttk.Frame(main_frame, style='Config.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(title_frame, text="Configuración", style='ConfigTitle.TLabel').pack(side=tk.LEFT)

        card_frame = ttk.Frame(main_frame, style='ConfigCard.TFrame')
        card_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        content_frame = ttk.Frame(card_frame, style='ConfigCard.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        button_frame = ttk.Frame(content_frame, style='ConfigCard.TFrame')
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        def open_student_edit():
            student_window = tk.Toplevel(self.window)
            CrudInterface(student_window, "documentos_base_de_datos.db")

        ttk.Button(
            button_frame, 
            text="Cancelar",
            style='ConfigAction.TButton',
            command=lambda: self.window.destroy()
        ).pack(side=tk.RIGHT, padx=(3, 0))

        try:
            ttk.Button(
                button_frame, 
                text="Edición de Estudiantes",
                style='ConfigAction.TButton',
                command=open_student_edit
            ).pack(side=tk.LEFT, padx=(1, 0))
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la ventana de edición de estudiantes: {str(e)}")

        self.window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())
        self.window.bind("<Destroy>", self._on_destroy)

    def _setup_styles(self) -> None:
        style = ttk.Style()
        colors = {
            'bg': '#F0F4F8',
            'fg': '#2D3748',
            'card_bg': '#FFFFFF',
            'button_bg': '#4299E1',
            'button_active': '#3182CE',
            'text_secondary': '#4A5568'
        }
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

    def _on_destroy(self, event=None):
        self.window = None

    def close_config_window(self):
        if self.window:
            self.window.grab_release()  # Liberar el grab para evitar bloquear la ventana principal
            self.window.destroy()
            self.window = None

    def get_config(self, key: str) -> str:
        return self.config.get(key, self.default_config.get(key, ""))
