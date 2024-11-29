import os 
import json
from datetime import datetime
from tkinter import Tk, filedialog
from .file_utils import get_last_sequence_number, save_last_sequence_number
from .template_manager import load_template, replace_placeholders
from .document_generator_ui import DocumentGeneratorUI

class DocumentGenerator:
    def __init__(self, parent=None):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.TEMPLATE_PATH = os.path.join(self.BASE_DIR, '..', 'Plantillas', 'CARTA DE PRES. 2024.docx')
        self.SEQUENCE_FILE = os.path.join(self.BASE_DIR, '..', '..', 'contador_documentos.json')
        self.ui = None
        self.on_close_callback = None
        self.parent = parent

    def initialize_ui(self):
        """Inicializa la interfaz de usuario"""
        if not self.ui:
            self.ui = DocumentGeneratorUI(self, self.parent)
            if self.on_close_callback:
                self.ui.set_on_close(self.on_close_callback)

    def generate_document(self, data):
        current_date = datetime.now()
        formatted_date = self._format_date(current_date)

        last_year, last_number = get_last_sequence_number(self.SEQUENCE_FILE)

        if current_date.year != last_year or current_date.year >= 2025:
            new_number = 1
        else:
            new_number = last_number + 1

        sequence_number_str = f"{new_number:04}"

        placeholders = {
            '{Fecha}': formatted_date,
            '{numero}': sequence_number_str,
            '{Anho}': str(current_date.year),
            '{Nombre_Receptor}': data['entry_receptor'],
            '{Descripcion}': data['entry_descripcion'],
            '{Nombre_Alumno}': data['entry_nombre_alumno'],
            '{N_Modulo}': data['entry_nu_modulo'],
            '{Nombre_Modulo}': data['entry_nombre_modulo'],
            '{Horas_Modulo}': data['entry_horas_modulo']
        }

        document = load_template(self.TEMPLATE_PATH)
        replace_placeholders(document, placeholders)

        file_name = self.ui.get_file_name()
        if file_name:
            file_path = self._get_output_file_path(file_name)
            if file_path and self._save_document(document, file_path):
                save_last_sequence_number(self.SEQUENCE_FILE, current_date.year, new_number)
                self.ui.clear_fields()
                self.ui.show_success_message(f"Documento {file_name}.docx generado exitosamente.")

    def _format_date(self, date):
        formatted_date = date.strftime("%d de %B del %Y")
        parts = formatted_date.split()
        parts[2] = parts[2].capitalize()
        return " ".join(parts)

    def _get_output_file_path(self, file_name):
        try:
            root = Tk()
            root.withdraw()  # Oculta la ventana principal de Tkinter
            docs_path = filedialog.askdirectory(title="Selecciona la ruta para guardar el documento")

            if not docs_path:
                self.ui.show_error_message("Ruta de documentos no seleccionada")
                return None

            file_path = os.path.join(docs_path, f'{file_name}.docx')
            counter = 1
            while os.path.exists(file_path):
                file_path = os.path.join(docs_path, f'{file_name}_{counter}.docx')
                counter += 1
            return file_path
        except Exception as e:
            self.ui.show_error_message(f"Error al obtener la ruta del archivo: {str(e)}")
            return None

    def _save_document(self, document, file_path):
        if not file_path:
            return False
            
        try:
            document.save(file_path)
            return True
        except Exception as e:
            self.ui.show_error_message(f"Error al guardar el documento: {str(e)}")
            return False

    def set_on_close(self, callback):
        """Establece el callback para cuando se cierra la ventana"""
        self.on_close_callback = callback
        if self.ui:
            self.ui.set_on_close(callback)

    def run(self):
        """Inicia la aplicación"""
        try:
            self.initialize_ui()
            if self.ui:
                self.ui.run()
            else:
                raise Exception("No se pudo inicializar la interfaz de usuario")
        except Exception as e:
            print(f"Error al iniciar la aplicación: {str(e)}")
            if self.on_close_callback:
                self.on_close_callback()
