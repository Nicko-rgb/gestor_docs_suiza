import os
import json
from datetime import datetime
from src.file_utils import get_last_sequence_number, save_last_sequence_number
from src.template_manager import load_template, replace_placeholders
from src.document_generator_ui import DocumentGeneratorUI

class DocumentGenerator:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.TEMPLATE_PATH = os.path.join(self.BASE_DIR, '..', 'Plantillas', 'CARTA DE PRES. 2024.docx')
        self.SEQUENCE_FILE = os.path.join(self.BASE_DIR, '..','..','contador_documentos.json')
        self.ruta_config = os.path.join(self.BASE_DIR, '..','..','config.json') # agregue esto 
        self.ui = None
        self.on_close_callback = None

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
            if self._save_document(document, file_path):
                save_last_sequence_number(self.SEQUENCE_FILE, current_date.year, new_number)
                self.ui.clear_fields()
                self.ui.show_success_message(f"Documento {file_name}.docx generado exitosamente.")
                
    def _format_date(self, date):
        formatted_date = date.strftime("%d de %B del %Y")
        parts = formatted_date.split()
        parts[2] = parts[2].capitalize()
        return " ".join(parts)

    def _get_output_file_path(self, file_name):
        with open(self.ruta_config, 'r') as file:
            config = json.load(file)
            docs_path = config.get('docs_path')

        if not docs_path:
            return None

        file_path = os.path.join(docs_path, f'{file_name}.docx')
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(docs_path, f'{file_name}_{counter}.docx')
            counter += 1
        return file_path

    def _save_document(self, document, file_path):
        try:
            document.save(file_path)
            return True
        except Exception as e:
            self.ui.show_error_message(f"Error al guardar el documento: {e}")
            return False

    def set_on_close(self, callback):
        self.on_close_callback = callback

    def run(self):
        self.ui = DocumentGeneratorUI(self)
        # self.ui.set_on_close(self.on_close)
        self.ui.run()

    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback()