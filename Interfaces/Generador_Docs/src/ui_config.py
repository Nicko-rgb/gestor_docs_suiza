UI_CONFIG = {
    "window": {
        "title": "Generador de Documento DOCX Estudiante",
        "width": 800,
        "height": 600
    },
    "colors": {
        "primary": "#F0F4F8",
        "secondary": "#2D3748",
        "accent": "#4299E1"
    },
    "fields": [
        {"label": "Nombre del Receptor:", "var_name": "entry_receptor"},
        {"label": "Cargo del Receptor:", "var_name": "entry_descripcion"},
        {"label": "Nombre Alumno:", "var_name": "entry_nombre_alumno"},
        {"label": "Número de Módulo:", "var_name": "entry_nu_modulo"},
        {"label": "Nombre Módulo:", "var_name": "entry_nombre_modulo"},
        {"label": "Horas de Módulo:", "var_name": "entry_horas_modulo"}
    ],
    "buttons": {
        "generate": {"text": "Generar Documento"},
        "reset": {"text": "Restablecer Contador"},
        "back": {"text": "Volver"}
    }
}