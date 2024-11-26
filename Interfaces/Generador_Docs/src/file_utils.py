import os
import json
from tkinter import messagebox
from datetime import datetime

def get_last_sequence_number(sequence_file):
    try:
        if os.path.exists(sequence_file):
            with open(sequence_file, 'r') as f:
                data = json.load(f)
                return data.get('ultimo_anio', datetime.now().year), data.get('ultimo_numero', 0)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo de contador: {e}")
    return datetime.now().year, 0

def save_last_sequence_number(sequence_file, year, number):
    try:
        with open(sequence_file, 'w') as f:
            json.dump({'ultimo_anio': year, 'ultimo_numero': number}, f)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el número de secuencia: {e}")
        return False