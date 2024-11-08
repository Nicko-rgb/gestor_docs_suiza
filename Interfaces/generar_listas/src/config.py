# config.py
import os
from typing import Dict, Any

# Configuración de la base de datos (fuera de la clase)
DB_CONFIG: Dict[str, str] = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'documentos_base_de_datos'
}

class Config:
    """Clase de configuración centralizada para la aplicación."""
    
    # Rutas base
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    PLANTILLA_PATH = os.path.join(BASE_DIR, 'Plantillas', 'ASISTENCIA_DIARIA.docx')
    
    # Configuración de la interfaz de usuario
    UI_CONFIG: Dict[str, Any] = {
        "window": {
            "title": "Generador de Asistencia",
            "width": 800,
            "height": 700
        },
        "colors": {
            "primary": "#F0F4F8",
            "secondary": "#2D3748",
            "accent": "#4299E1",
            "background": "#FFFFFF",
            "text": "#4A5568",
            "border": "#E2E8F0"
        },
        "buttons": {
            "show": {"text": "Mostrar Estudiantes"},
            "generate": {"text": "Generar Documento"},
            "back": {"text": "Regresar"},
            "close": {"text": "Cerrar"},
            "return": {"text": "Volver"}
        },
        "fonts": {
            "title": ("Segoe UI", 24, "bold"),
            "subtitle": ("Segoe UI", 16, "bold"),
            "body": ("Segoe UI", 12),
            "small": ("Segoe UI", 10),
            "footer": ("Segoe UI", 8)
        }
    }