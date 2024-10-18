import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import mysql.connector
import os
from datetime import datetime
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.section import WD_ORIENT
import locale
from typing import List, Tuple, Dict, Optional
import logging

class DatabaseManager:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='documentos_base_de_datos'
            )
            return self.connection
        except mysql.connector.Error as e:
            logging.error(f"Database connection error: {e}")
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return None

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        if not self.connection:
            self.connect()
        
        if self.connection:
            with self.connection.cursor() as cursor:
                try:
                    cursor.execute(query, params or ())
                    return cursor.fetchall()
                except mysql.connector.Error as e:
                    logging.error(f"Query execution error: {e}")
                    messagebox.showerror("Error", f"Error al ejecutar el query: {e}")
        return []

    def close(self):
        if self.connection:
            self.connection.close()

class DocumentGenerator:
    def __init__(self, template_path: str):
        self.template_path = template_path

    def load_template(self) -> Optional[Document]:
        try:
            return Document(self.template_path)
        except Exception as e:
            logging.error(f"Error loading template: {e}")
            messagebox.showerror("Error", f"Error al cargar la plantilla: {e}")
            return None

    @staticmethod
    def replace_placeholders(doc: Document, placeholders: Dict[str, str]):
        for element in doc.element.body.iter():
            if element.text:
                for placeholder, value in placeholders.items():
                    if placeholder in element.text:
                        element.text = element.text.replace(placeholder, value)

    @staticmethod
    def save_document(doc: Document, output_path: str) -> bool:
        try:
            doc.save(output_path)
            return True
        except Exception as e:
            logging.error(f"Error saving document: {e}")
            messagebox.showerror("Error", f"Error al guardar el documento: {e}")
            return False

    @staticmethod
    def set_cell_border(cell, border_size: int = 4):
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcBorders = tcPr.first_child_found_in("w:tcBorders")
        if tcBorders is None:
            tcBorders = OxmlElement('w:tcBorders')
            tcPr.append(tcBorders)
        for border in ['top', 'left', 'bottom', 'right']:
            border_elem = OxmlElement(f'w:{border}')
            border_elem.set(qn('w:val'), 'single')
            border_elem.set(qn('w:sz'), str(border_size))
            border_elem.set(qn('w:space'), '0')
            border_elem.set(qn('w:color'), '000000')
            tcBorders.append(border_elem)

class GeneradorAsistencia:
    def __init__(self, parent):
        self.parent = parent
        self.root = None
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.PLANTILLA_PATH = os.path.join(self.BASE_DIR, 'Interfaces', 'Plantillas', 'ASISTENCIA_DIARIA.docx')
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        self.on_close_callback = None
        self.db_manager = DatabaseManager()
        self.doc_generator = DocumentGenerator(self.PLANTILLA_PATH)
        
        self.UI_CONFIG = {
            "window": {"title": "Generador de Asistencia", "width": 800, "height": 700},
            "colors": {"primary": "#F0F4F8", "secondary": "#2D3748", "accent": "#4299E1"},
            "buttons": {
                "show": {"text": "Mostrar Estudiantes"},
                "generate": {"text": "Generar Documento"},
                "back": {"text": "Regresar"},
                "close": {"text": "Cerrar"},
                "return": {"text": "Volver"}
            }
        }
        
        self.combo_ciclo = None
        self.combo_profesor = None
        self.combo_curso = None
        self.tabla = None

    def obtener_ciclos(self) -> List[Tuple]:
        return self.db_manager.execute_query("SELECT ID_CICLO, NRO_CICLO FROM ciclo")

    def obtener_profesores(self) -> List[Tuple]:
        return self.db_manager.execute_query("SELECT ID_PROFESOR, NOMBRE, APELLIDO FROM profesores")

    def obtener_cursos(self) -> List[Tuple]:
        return self.db_manager.execute_query("SELECT ID_CURSO, NOMBRE_CURSO FROM curso")

    def extraer_estudiantes_por_ciclo(self):
        ciclo_id = self.combo_ciclo.get().split(" - ")[0]
        estudiantes = self.db_manager.execute_query('''
            SELECT APELLIDO_P, APELLIDO_M, NOMBRE
            FROM estudiantes_del_dsi 
            WHERE ID_CICLO = %s
        ''', (ciclo_id,))

        self.tabla.delete(*self.tabla.get_children())
        for idx, estudiante in enumerate(estudiantes, start=1):
            nombre_completo = f"{estudiante[0]} {estudiante[1]}, {estudiante[2]}"
            self.tabla.insert("", "end", values=(idx, nombre_completo))

    def generar_documento(self):
        fecha_actual = datetime.now().strftime('%d/%m/%Y')
        ano_actual = str(datetime.now().year)
        documento_original = self.doc_generator.load_template()
    
        if not documento_original:
            return

        section = documento_original.sections[0]
        section.orientation = WD_ORIENT.PORTRAIT
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)

        documento_original.add_paragraph("", style='Normal')
        tabla_word = documento_original.add_table(rows=1, cols=4)
        
        tabla_word.alignment = WD_TABLE_ALIGNMENT.CENTER

        headers = ["N°", "APELLIDO Y NOMBRE", "DNI", "FIRMA"]
        for i, header in enumerate(headers):
            tabla_word.cell(0, i).text = header
            self.doc_generator.set_cell_border(tabla_word.cell(0, i))

        widths = [Cm(1), Cm(9), Cm(3), Cm(3)]
        for i, width in enumerate(widths):
            tabla_word.columns[i].width = width

        filas = self.tabla.get_children()
        font_size = 11
        max_rows = 35

        while True:
            for _ in range(len(tabla_word.rows) - 1):
                tabla_word._element.remove(tabla_word.rows[-1]._element)

            for idx, fila in enumerate(filas, start=1):
                valores = self.tabla.item(fila)['values']
                nombre_completo = valores[1]
                row_cells = tabla_word.add_row().cells
                row_cells[0].text = str(idx)
                row_cells[1].text = nombre_completo
                row_cells[2].text = ""
                row_cells[3].text = ""
                
                for cell in row_cells:
                    self.doc_generator.set_cell_border(cell)
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.size = Pt(font_size)

            if len(tabla_word.rows) <= max_rows:
                break
            else:
                font_size -= 0.5
                if font_size < 8:
                    messagebox.showwarning("Advertencia", "No se puede ajustar la tabla a una sola página. Algunos datos pueden no ser visibles.")
                    break

        datos = {
            '{fecha}': fecha_actual,
            '{ano}': ano_actual,
        }

        nombre_archivo = simpledialog.askstring("Guardar como", "Introduce el nombre del archivo (sin extensión):")
        if not nombre_archivo:
            return 

        nombre_archivo = nombre_archivo.strip().replace(' ', '_')
        ruta_salida = os.path.join(self.BASE_DIR, f'{nombre_archivo}.docx')

        contador = 1
        while os.path.exists(ruta_salida):
            ruta_salida = os.path.join(self.BASE_DIR, f'{nombre_archivo}_{contador}.docx')
            contador += 1

        self.doc_generator.replace_placeholders(documento_original, datos)

        if self.doc_generator.save_document(documento_original, ruta_salida):
            messagebox.showinfo("Éxito", f"Documento guardado como {ruta_salida}")

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background=self.UI_CONFIG["colors"]["primary"])
        style.configure('TLabel', background=self.UI_CONFIG["colors"]["primary"], foreground=self.UI_CONFIG["colors"]["secondary"], font=('Segoe UI', 12))
        style.configure('TButton', font=('Segoe UI', 10))
        
        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), foreground=self.UI_CONFIG["colors"]["secondary"])
        
        style.configure('Card.TFrame', background='#FFFFFF', relief='flat')
        style.configure('CardTitle.TLabel', background='#FFFFFF', foreground=self.UI_CONFIG["colors"]["secondary"], font=('Segoe UI', 16, 'bold'))
        style.configure('CardBody.TLabel', background='#FFFFFF', foreground='#4A5568', font=('Segoe UI', 10))
        style.configure('Card.TButton', background=self.UI_CONFIG["colors"]["accent"], foreground='white', font=('Segoe UI', 10, 'bold'))
        style.map('Card.TButton', background=[('active', '#3182CE')])

        style.configure('Footer.TButton', background='#E2E8F0', foreground='#4A5568', font=('Segoe UI', 9))
        style.map('Footer.TButton', background=[('active', '#CBD5E0')])

    def centro_ventana(self, ventana, ancho, alto):
        x = (ventana.winfo_screenwidth() - ancho) // 2
        y = (ventana.winfo_screenheight() - alto) // 2
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        self.root = tk.Toplevel(self.parent)
        self.root.title(self.UI_CONFIG["window"]["title"])
        self.centro_ventana(self.root, self.UI_CONFIG["window"]["width"], self.UI_CONFIG["window"]["height"])
        self.configurar_estilos()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)

        ttk.Label(main_frame, text="Generador de Lista de Asistencia", style='Title.TLabel').pack(pady=(0, 40))

        card_frame = ttk.Frame(main_frame, style='Card.TFrame')
        card_frame.pack(fill='both', expand=True, padx=20, pady=20)

        combo_frame = ttk.Frame(card_frame)
        combo_frame.pack(fill='x', pady=10)

        ttk.Label(combo_frame, text="Ciclo:", style='CardBody.TLabel', width=10).pack(side='left', padx=(0, 10))
        self.combo_ciclo = ttk.Combobox(combo_frame, state="readonly", width=30)
        self.combo_ciclo.pack(side='left', padx=(0, 20))

        ttk.Label(combo_frame, text="Profesor:", style='CardBody.TLabel', width=10).pack(side='left', padx=(0, 10))
        self.combo_profesor = ttk.Combobox(combo_frame, state="readonly", width=30)
        self.combo_profesor.pack(side='left')

        curso_frame = ttk.Frame(card_frame)
        curso_frame.pack(fill='x', pady=10)

        ttk.Label(curso_frame, text="Curso:", style='CardBody.TLabel', width=10).pack(side='left', padx=(0, 10))
        self.combo_curso = ttk.Combobox(curso_frame, state="readonly", width=30)
        self.combo_curso.pack(side='left')

        button_frame = ttk.Frame(card_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text=self.UI_CONFIG["buttons"]["show"]["text"], style='Card.TButton', 
                   command=self.extraer_estudiantes_por_ciclo).pack(side='left', padx=10)
        ttk.Button(button_frame, text=self.UI_CONFIG["buttons"]["generate"]["text"], style='Card.TButton', 
                   command=self.generar_documento).pack(side='left', padx=10)

        tree_frame = ttk.Frame(card_frame)
        tree_frame.pack(fill='both', expand=True, pady=10)

        columns = ("N°", "APELLIDO_Y_NOMBRE")
        self.tabla = ttk.Treeview(tree_frame, columns=columns, show='headings')
        for col in columns:
            self.tabla.heading(col, text=col)
        self.tabla.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side='right', fill='y')
        self.tabla.configure(yscrollcommand=scrollbar.set)

        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side='bottom', fill='x', pady=(20, 0))

        ttk.Label(footer_frame, text="© 2024 Sistema de Gestor de Documentos", 
                  font=('Segoe UI', 8)).pack(side='left')

        button_frame = ttk.Frame(footer_frame)
        button_frame.pack(side='right')

        ttk.Button(button_frame, text=self.UI_CONFIG["buttons"]["close"]["text"], style='Footer.TButton', 
                   command=self.root.destroy).pack(side='right', padx=(0, 10))

        ttk.Button(button_frame, text=self.UI_CONFIG["buttons"]["return"]["text"], style='Footer.TButton', 
                   command=self.volver).pack(side='right', padx=(0, 10))

        # Ciclos
        ciclos = self.obtener_ciclos()
        if ciclos:
            self.combo_ciclo['values'] = [f"{ciclo[0]} - {ciclo[1]}" for ciclo in ciclos]
        
        # Profesores
        profesores = self.obtener_profesores()
        if profesores:
            self.combo_profesor['values'] = [f"{profesor[1]} {profesor[2]}" for profesor in profesores]
        
        # Cursos
        cursos = self.obtener_cursos()
        if cursos:
            self.combo_curso['values'] = [curso[1] for curso in cursos]
            

    def volver(self):
        self.tabla.delete(*self.tabla.get_children())
        self.combo_ciclo.set('')
        self.combo_profesor.set('')
        self.combo_curso.set('')
        self.root.destroy()
        if self.on_close_callback:
            self.on_close_callback()
    
    def set_on_close(self, callback):
        self.on_close_callback = callback
        
    def run(self):
        self.crear_interfaz()
        self.root.protocol("WM_DELETE_WINDOW", self.volver)  # Manejar el cierre de la ventana
        self.root.grab_set()
        self.root.wait_window()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    generator = GeneradorAsistencia(root)
    generator.run()
    root.destroy()