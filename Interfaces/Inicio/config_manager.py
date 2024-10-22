# config_manager.py
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict, Optional

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
        """Carga la configuración desde el archivo JSON."""
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
        """Guarda la configuración en el archivo JSON."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la configuración: {str(e)}")

    def browse_directory(self, entry: ttk.Entry) -> None:
        """Abre el diálogo para seleccionar directorio."""
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)

    def show_config_window(self) -> None:
        """Muestra la ventana de configuración."""
        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            return

        self.window = tk.Toplevel(self.parent)
        self.window.title("Configuración")
        self.window.geometry("400x300")
        self.window.resizable(False, False)

        # Hacer la ventana modal
        self.window.transient(self.parent)
        self.window.grab_set()

        # Configurar el estilo
        style = ttk.Style()
        style.configure('Config.TFrame', padding=(20, 20, 20, 20))
        style.configure('Config.TLabel', padding=(0, 5))
        style.configure('Config.TButton', padding=(5, 5))

        main_frame = ttk.Frame(self.window, style='Config.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear los campos de configuración
        paths = [
            ("Ruta de Generador de Carta de Presentación:", "docs_path"),
            ("Ruta de Generador de Lista:", "output_path")
        ]

        entries = {}
        for i, (label_text, config_key) in enumerate(paths):
            # Frame para cada fila
            row_frame = ttk.Frame(main_frame)
            row_frame.pack(fill=tk.X, pady=5)

            # Label
            ttk.Label(row_frame, text=label_text, style='Config.TLabel').pack(side=tk.LEFT)
            
            # Entry
            entry = ttk.Entry(row_frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
            if self.config[config_key]:
                entry.insert(0, self.config[config_key])
            entries[config_key] = entry

            # Botón Browse
            ttk.Button(row_frame, text="...", 
                      command=lambda e=entry: self.browse_directory(e),
                      style='Config.TButton', width=3).pack(side=tk.LEFT)

        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))

        def save_and_close():
            for key, entry in entries.items():
                self.config[key] = entry.get()
            self.save_config()
            self.window.destroy()
            self.window = None

        ttk.Button(button_frame, text="Guardar", 
                  command=save_and_close,
                  style='Config.TButton').pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=lambda: self.window.destroy(),
                  style='Config.TButton').pack(side=tk.RIGHT, padx=5)

        # Manejar el cierre de la ventana
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())
        self.window.bind("<Destroy>", self._on_destroy)

    def _on_destroy(self, event=None):
        """Maneja la destrucción de la ventana de configuración."""
        self.window = None

    def get_config(self, key: str) -> str:
        """Obtiene un valor de configuración específico."""
        return self.config.get(key, self.default_config.get(key, ""))
