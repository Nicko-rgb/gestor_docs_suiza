import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any
from src.document import DocumentGenerator
from src.db_manager import DatabaseManager
from src.base_components import ComboBoxGroup, CustomTable, Footer
from src.config import Config
from src.styles import StyleManager
from datetime import datetime
import sys
import os

class GeneradorAsistencia:
    """Clase principal para la generación de documentos de asistencia."""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.window: Optional[tk.Toplevel] = None
        self.db = DatabaseManager()
        self.style_manager = StyleManager()
        self.selected_data: Dict[str, Any] = {}
        self.curso_profesor_map = {}  # Mapeo de cursos a profesores
        self.on_close_callback = None  # Callback para cuando se cierre la ventana
        
        
    def run(self):
        """Inicializa y muestra la ventana principal."""
        self.window = tk.Toplevel(self.root)
        self._configure_window()
        self._initialize_components()
        self._load_initial_data()
        
    def _configure_window(self):
        """Configura las propiedades de la ventana."""
        config = Config.UI_CONFIG["window"]
        self.window.title(config["title"])
        self.window.geometry(f"{config['width']}x{config['height']}")
        self.window.configure(bg=Config.UI_CONFIG["colors"]["primary"])
        self.style_manager.configure_styles()
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - config["width"]) // 2
        y = (screen_height - config["height"]) // 2
        self.window.geometry(f"+{x}+{y}")   
        
    def _initialize_components(self):
        """Inicializa todos los componentes de la interfaz."""
        # Contenedor principal
        self.main_frame = ttk.Frame(self.window, style='TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        self.title = ttk.Label(
            self.main_frame,
            text="Generador de Asistencia",
            style='Title.TLabel'
        )
        self.title.pack(pady=(0, 20))
        
        # Card de selección
        self.selection_card = ttk.Frame(self.main_frame, style='Card.TFrame')
        self.selection_card.pack(fill='x', padx=20, pady=10)
        
        # Comboboxes
        self.ciclo_combo = ComboBoxGroup(
            self.selection_card,
            "Ciclo",
            width=40
        )
        self.ciclo_combo.pack(pady=10)
        self.ciclo_combo.bind('<<ComboboxSelected>>', self._on_ciclo_selected)
        
        self.curso_combo = ComboBoxGroup(
            self.selection_card,
            "Curso",
            width=40
        )
        self.curso_combo.pack(pady=10)
        self.curso_combo.bind('<<ComboboxSelected>>', self._on_curso_selected)

        self.profesor_combo = ComboBoxGroup(
            self.selection_card,
            "Profesor",
            width=40,
            state="readonly"  # Hacer el campo de solo lectura
        )
        self.profesor_combo.pack(pady=10)
        
        # Tabla de estudiantes
        self.table = CustomTable(
            self.main_frame,
            ("ID", "DNI", "Nombre", "Apellido P", "Apellido M", "Email", "Teléfono")
        )
        self.table.pack(fill='both', expand=True, pady=20)
        
        # Botones de acción
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill='x', pady=20)
        
        self.generate_btn = ttk.Button(
            self.button_frame,
            text=Config.UI_CONFIG["buttons"]["generate"]["text"],
            style='Card.TButton',
            command=self._generate_document
        )
        self.generate_btn.pack(side='right', padx=5)
        
        # Footer
        self.footer = Footer(
            self.main_frame,
            self._on_return,
            self._on_close
        )
        self.footer.pack()
        
    def _load_initial_data(self):
        """Carga los datos iniciales en los comboboxes."""
        try:
            # Cargar ciclos
            ciclos = self.db.execute_query("""
                SELECT ID_CICLO, NRO_CICLO 
                FROM ciclo 
                ORDER BY NRO_CICLO ASC
            """)
            self.ciclo_combo.combobox['values'] = [f"{c[1]}" for c in ciclos]
            
            # Crear mapeo de cursos a profesores
            curso_profesor_data = self.db.execute_query("""
                SELECT c.NOMBRE_CURSO, p.NOMBRE_PROFESOR, p.APELLIDOS_PROFESOR, c.ID_PROFESOR
                FROM curso c
                JOIN profesores p ON c.ID_PROFESOR = p.ID_PROFESOR
            """)
            
            self.curso_profesor_map = {
                curso: (f"{nombre} {apellidos}", id_profesor)
                for curso, nombre, apellidos, id_profesor in curso_profesor_data
            }
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos iniciales: {e}")
    
    def _on_ciclo_selected(self, event):
        """Maneja la selección de ciclo y carga los cursos correspondientes."""
        ciclo = self.ciclo_combo.get()
        self.curso_combo.set('')
        self.profesor_combo.set('')
        self.table.clear()
        
        if not ciclo:
            return
            
        try:
            # Obtener los cursos del ciclo seleccionado
            cursos = self.db.execute_query("""
                SELECT DISTINCT c.NOMBRE_CURSO 
                FROM curso c
                WHERE c.ID_CICLO = (SELECT ID_CICLO FROM ciclo WHERE NRO_CICLO = %s)
                ORDER BY c.NOMBRE_CURSO
            """, (ciclo,))
            
            # Actualizar el combobox de cursos
            self.curso_combo.combobox['values'] = [curso[0] for curso in cursos]
            
            if not cursos:
                messagebox.showwarning(
                    "Aviso", 
                    "No se encontraron cursos para este ciclo"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los cursos: {e}")
    
    def _on_curso_selected(self, event):
        """Maneja la selección del curso y actualiza el profesor y la lista de estudiantes."""
        curso = self.curso_combo.get()
        ciclo = self.ciclo_combo.get()
        
        if not curso or not ciclo:
            return
            
        try:
            # Autocompletar el profesor basado en el curso seleccionado
            if curso in self.curso_profesor_map:
                profesor_nombre, _ = self.curso_profesor_map[curso]
                self.profesor_combo.set(profesor_nombre)
            
            # Obtener estudiantes del ciclo seleccionado
            estudiantes = self.db.execute_query("""
                SELECT ID_ESTUDIANTE, DNI, NOMBRE, APELLIDO_P, APELLIDO_M, 
                       CORREO, NUMERO_TELEFONO
                FROM estudiantes_del_dsi 
                WHERE ID_CICLO = (SELECT ID_CICLO FROM ciclo WHERE NRO_CICLO = %s)
            """, (ciclo,))
            
            self.table.clear()
            for estudiante in estudiantes:
                self.table.insert(estudiante)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos del curso: {e}")
    
    def _generate_document(self):
        """Genera el documento de asistencia."""
        if not all([self.ciclo_combo.get(), self.profesor_combo.get(), self.curso_combo.get()]):
            messagebox.showerror("Error", "Debe seleccionar todos los campos")
            return
            
        try:
            doc = DocumentGenerator.load_template(Config.PLANTILLA_PATH)
            print(doc.paragraphs[0].text)
            print(doc.paragraphs[1].text)
            print(doc.paragraphs[2].text)
            if not doc:
                return
                
            # Obtener la hora de inicio del curso seleccionado
            curso_seleccionado = self.curso_combo.get()
            hora_inicio_curso = self.db.execute_query("""
                SELECT HORA_INICIO 
                FROM curso
                WHERE NOMBRE_CURSO = %s
            """, (curso_seleccionado,))[0][0]

            # Convertir el objeto timedelta a una cadena de texto en el formato deseado
            hora_inicio_curso_str = f"{hora_inicio_curso.seconds // 3600}:{(hora_inicio_curso.seconds // 60) % 60:02d}"

            placeholders = {
                "{docente}": self.profesor_combo.get(),
                "{ciclo}": self.ciclo_combo.get(), 
                "{anho}": datetime.now().strftime("%Y"),
                "{unidad}": self.curso_combo.get(),
                "{fecha}": datetime.now().strftime("%d/%m/%Y"),
                "{hora}": hora_inicio_curso_str
            }
            
            DocumentGenerator.replace_placeholders(doc, placeholders)
            # Obtener estudiantes de la tabla
            estudiantes = []
            for item in self.table.tree.get_children():
                values = self.table.tree.item(item)['values']
                # Obtener apellidos y nombre de las columnas correctas
                estudiantes.append((values[3], values[4], values[2])) # apellido_p, apellido_m, nombre
                
            # Crear lista de asistencia con los estudiantes
            doc = DocumentGenerator.create_attendance_list(doc, estudiantes)
            
            output_path = f"Asistencia_{self.ciclo_combo.get()}_{self.curso_combo.get()}.docx"
            if DocumentGenerator.save_document(doc, output_path):
                messagebox.showinfo("Éxito", f"Documento generado exitosamente: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar documento: {e}")
    #modifque esta funcion
    def set_on_close(self, callback):
        """Establece el callback para cuando se cierre la ventana."""
        self.on_close_callback = callback
        
    def _on_return(self):
        """Maneja el evento de retorno al menú principal."""
       
        self.window.destroy()
            
        self.on_close_callback()
    
    def _on_close(self):
        """Maneja el evento de cierre de la aplicación."""
        if messagebox.askyesno("Confirmar", "¿Desea cerrar la aplicación?"):
            self.window.quit()
            self.root.quit()