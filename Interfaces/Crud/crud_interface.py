import tkinter as tk
from tkinter import ttk, messagebox
from Crud.crud import Crud
from Crud.Config import DB_CONFIG
import logging
from PIL import Image, ImageTk

class CrudInterface:
    def __init__(self, master, db_config):
        self.master = master
        self.db_config = DB_CONFIG
        # Inicializar selected_cycle aquí
        self.selected_cycle = None
        self.crud = None
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        try:
            self._setup_styles()
            self.setup_ui()
        except Exception as e:
            self.logger.error(f"Error al inicializar la interfaz: {e}")
            messagebox.showerror("Error", f"Error al inicializar la interfaz: {e}")

    def _setup_styles(self):
        """Configura los estilos de la interfaz."""
        style = ttk.Style()
        style.theme_use('clam')

        # Configuración de colores
        self.colors = {
            'bg': '#F0F4F8',
            'fg': '#2D3748',
            'card_bg': '#FFFFFF',
            'button_bg': '#4299E1',
            'button_active': '#3182CE',
            'text_secondary': '#4A5568',
            'header_bg': '#E2E8F0',
            'success': '#48BB78',
            'warning': '#ED8936',
            'danger': '#F56565'
        }

        # Estilos base
        style.configure('Main.TFrame', background=self.colors['bg'])
        style.configure('Card.TFrame', background=self.colors['card_bg'])
        
        # Estilo para el Treeview
        style.configure('Treeview',
                       background=self.colors['card_bg'],
                       foreground=self.colors['fg'],
                       fieldbackground=self.colors['card_bg'],
                       font=('Segoe UI', 10))
        
        style.configure('Treeview.Heading',
                       background=self.colors['header_bg'],
                       foreground=self.colors['fg'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Estilos de botones
        style.configure('Action.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['button_bg'],
                       foreground='white')
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['success'])
        
        style.configure('Warning.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['warning'])
        
        style.configure('Danger.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['danger'])
        
        style.map('Action.TButton',
                 background=[('active', self.colors['button_active'])])
        
        # Estilo para el título
        style.configure('Title.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       background=self.colors['bg'],
                       foreground=self.colors['fg'])

    def setup_ui(self):
        """Configura la interfaz de usuario."""
        self.master.title("Edición de Estudiantes")
        
        # Configuración de la ventana
        window_width = 1100
        window_height = 600
        x = (self.master.winfo_screenwidth() - window_width) // 2
        y = (self.master.winfo_screenheight() - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.master.resizable(False, False)
        self.master.overrideredirect(1)
        
        # Frame principal
        main_frame = ttk.Frame(self.master, style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_frame = ttk.Frame(main_frame, style='Main.TFrame')
        title_frame.pack(fill=tk.X, padx=40, pady=(20, 0))
        
        # Logo
        try:
            image = Image.open("gestor_docs_suiza/Imagenes/logoDSI.png")
            image = image.resize((80, 80))
            self.photo = ImageTk.PhotoImage(image)
            logo_label = ttk.Label(title_frame, image=self.photo, background=self.colors['bg'])
            logo_label.pack(side=tk.LEFT, padx=(0, 20))
        except Exception as e:
            self.logger.warning(f"No se pudo cargar el logo: {e}")

        ttk.Label(title_frame, 
                 text="Gestión de Estudiantes",
                 style='Title.TLabel').pack(side=tk.LEFT, pady=20)

        # Frame para operaciones CRUD
        crud_frame = ttk.Frame(main_frame, style='Card.TFrame', padding=10)
        crud_frame.pack(fill=tk.X, padx=40, pady=(20, 10))

        # Botones CRUD
        ttk.Button(crud_frame, 
                  text="Agregar Estudiante",
                  style='Success.TButton',
                  command=self.show_add_dialog).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(crud_frame,
                  text="Editar Estudiante",
                  style='Warning.TButton',
                  command=self.show_edit_dialog).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(crud_frame,
                  text="Eliminar Estudiante",
                  style='Danger.TButton',
                  command=self.delete_student).pack(side=tk.LEFT, padx=5)
        
        # Frame derecho para el filtro de ciclos
        filter_frame = ttk.Frame(crud_frame)
        filter_frame.pack(side=tk.RIGHT, fill=tk.X, padx=(20, 0))

        ttk.Label(filter_frame, 
                 text="Filtrar por Ciclo:",
                 style='Main.TLabel').pack(side=tk.LEFT, padx=(0, 10))

        self.cycle_combobox = ttk.Combobox(filter_frame, width=15)
        self.cycle_combobox.pack(side=tk.LEFT)
        self.load_cycles()  # Cargar los ciclos disponibles
        self.cycle_combobox.bind('<<ComboboxSelected>>', self.on_cycle_selected)

        # Frame para el Treeview
        tree_frame = ttk.Frame(main_frame, style='Card.TFrame', padding=20)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(10, 20))

        # Configurar columnas
        columns = ("ID", "DNI", "Nombre", "Apellido P", "Apellido M", 
                  "Correo", "Número", "Dirección", "Ciclo")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                style='Treeview')
        
        # Configurar scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, 
                                command=self.tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL,
                                command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set,
                          xscrollcommand=x_scroll.set)
        
        # Empaquetar scrollbars
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configurar columnas del Treeview
        column_widths = {
            "ID": 30, "DNI": 100, "Nombre": 100,
            "Apellido P": 100, "Apellido M": 100,
            "Correo": 120, "Número": 80,
            "Dirección": 80, "Ciclo": 30
        }
        
        for col in columns:
            self.tree.column(col, width=column_widths[col], minwidth=50)
            self.tree.heading(col, text=col)

        # Frame para botones
        button_frame = ttk.Frame(main_frame, style='Main.TFrame')
        button_frame.pack(fill=tk.X, padx=40, pady=(0, 20))

        # Botones
        ttk.Button(button_frame, text="Volver", 
                  style='Action.TButton',
                  command=self.master.destroy).pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="Cerrar",
                  style='Action.TButton', 
                  command=self.master.destroy).pack(side=tk.RIGHT)

        self.load_data()
    
    def load_cycles(self):
        """Carga los ciclos disponibles en el combobox."""
        try:
            crud = Crud(self.db_config)
            cycles = crud.fetch_all_cycles()  # Necesitarás implementar este método en tu clase Crud
            cycle_values = ["Todos"] + [str(cycle[0]) for cycle in cycles]  # Asumiendo que cycle[0] es el número de ciclo
            self.cycle_combobox['values'] = cycle_values
            self.cycle_combobox.set("Todos")  # Valor por defecto
        except Exception as e:
            self.logger.error(f"Error al cargar ciclos: {e}")
            messagebox.showerror("Error", f"Error al cargar ciclos: {e}")
        finally:
            if 'crud' in locals():
                crud.close()

    def on_cycle_selected(self, event):
        """Maneja el evento de selección de ciclo."""
        selected = self.cycle_combobox.get()
        self.selected_cycle = None if selected == "Todos" else selected
        self.load_data()

    def show_add_dialog(self):
        """Muestra el diálogo para agregar un estudiante."""
        dialog = tk.Toplevel(self.master)
        dialog.title("Agregar Estudiante")
        
        # Configurar el tamaño y posición
        dialog_width = 500
        dialog_height = 500
        x = self.master.winfo_x() + (self.master.winfo_width() - dialog_width) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - dialog_height) // 2
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        dialog.transient(self.master)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Frame principal del diálogo
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, 
                text="Agregar Nuevo Estudiante",
                font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Frame para los campos
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True)

        # Configuración de la cuadrícula
        fields_frame.columnconfigure(1, weight=1)  # La columna de entries se expandirá
        
        # Crear campos de entrada con labels
        fields = [
            ("DNI:", "DNI"),
            ("Nombre:", "Nombre"),
            ("Apellido Paterno:", "Apellido P"),
            ("Apellido Materno:", "Apellido M"),
            ("Correo electrónico:", "Correo"),
            ("Número telefónico:", "Número"),
            ("Dirección:", "Dirección"),
            ("Ciclo:", "ID Ciclo")
        ]
        
        entries = {}
        for i, (label_text, field_key) in enumerate(fields):
            # Label
            label = ttk.Label(fields_frame, text=label_text)
            label.grid(row=i, column=0, sticky='e', padx=(0, 10), pady=5)
            
            # Entry
            entry = ttk.Entry(fields_frame)
            entry.grid(row=i, column=1, sticky='ew', pady=5)
            entries[field_key] = entry

        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))

        def save():
            data = {field: entries[field].get() for field in dict(fields).values()}
            try:
                crud = Crud(self.db_config)
                crud.add_student(data)
                messagebox.showinfo("Éxito", "Estudiante agregado correctamente")
                dialog.destroy()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Error al agregar estudiante: {e}")
            finally:
                if 'crud' in locals():
                    crud.close()

        def cancel():
            dialog.destroy()

        # Botones
        cancel_btn = ttk.Button(button_frame, text="Cancelar", command=cancel)
        cancel_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        save_btn = ttk.Button(button_frame, text="Guardar", command=save)
        save_btn.pack(side=tk.LEFT, padx=5, expand=True)

    def show_edit_dialog(self):
        """Muestra el diálogo para editar un estudiante."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", 
                                "Por favor, seleccione un estudiante para editar")
            return

        values = self.tree.item(selected[0])['values']
        
        dialog = tk.Toplevel(self.master)
        dialog.title("Editar Estudiante")
        
        dialog_width = 500
        dialog_height = 550
        x = self.master.winfo_x() + (self.master.winfo_width() - dialog_width) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - dialog_height) // 2
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        dialog.transient(self.master)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Frame principal
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, 
                text="Editar Estudiante",
                font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Frame para los campos
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True)

        # Configuración de la cuadrícula
        fields_frame.columnconfigure(1, weight=1)
        
        # Crear campos
        fields = [
            ("ID:", "ID"),
            ("DNI:", "DNI"),
            ("Nombre:", "Nombre"),
            ("Apellido Paterno:", "Apellido P"),
            ("Apellido Materno:", "Apellido M"),
            ("Correo electrónico:", "Correo"),
            ("Número telefónico:", "Número"),
            ("Dirección:", "Dirección"),
            ("Ciclo:", "ID Ciclo")
        ]
        
        entries = {}
        for i, (label_text, field_key) in enumerate(fields):
            # Label
            label = ttk.Label(fields_frame, text=label_text)
            label.grid(row=i, column=0, sticky='e', padx=(0, 10), pady=5)
            
            # Entry
            entry = ttk.Entry(fields_frame)
            entry.insert(0, values[i])
            if field_key == "ID":
                entry.configure(state='readonly')
            entry.grid(row=i, column=1, sticky='ew', pady=5)
            entries[field_key] = entry

        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))

        def save():
            data = {field: entries[field].get() for field in dict(fields).values()}
            try:
                crud = Crud(self.db_config)
                crud.update_student(data)
                messagebox.showinfo("Éxito", "Estudiante actualizado correctamente")
                dialog.destroy()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar estudiante: {e}")
            finally:
                if 'crud' in locals():
                    crud.close()

        def cancel():
            dialog.destroy()

        # Botones
        cancel_btn = ttk.Button(button_frame, text="Cancelar", command=cancel)
        cancel_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        save_btn = ttk.Button(button_frame, text="Guardar", command=save)
        save_btn.pack(side=tk.LEFT, padx=5, expand=True)

    def delete_student(self):
        """Elimina el estudiante seleccionado."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia",
                                 "Por favor, seleccione un estudiante para eliminar")
            return

        if messagebox.askyesno("Confirmar eliminación",
                              "¿Está seguro de que desea eliminar este estudiante?"):
            student_id = self.tree.item(selected[0])['values'][0]
            
            try:
                crud = Crud(self.db_config)
                crud.delete_student(student_id)
                messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
                self.load_data()  # Recargar datos
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar estudiante: {e}")
            finally:
                if 'crud' in locals():
                    crud.close()

    def load_data(self):
        """Carga los datos en el Treeview según el filtro seleccionado."""
        # Limpiar datos existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self.crud = Crud(self.db_config)
            if hasattr(self, 'selected_cycle') and self.selected_cycle:
                rows = self.crud.fetch_students_by_cycle(self.selected_cycle)
            else:
                rows = self.crud.fetch_all_students()
                
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            error_msg = f"Error al cargar datos: {e}"
            self.logger.error(error_msg)
            messagebox.showerror("Error", error_msg)
        finally:
            if self.crud:
                self.crud.close()
                self.crud = None
    
    def load_cycles(self):
        """Carga los ciclos disponibles en el combobox."""
        try:
            self.crud = Crud(self.db_config)
            cycles = self.crud.fetch_all_cycles()
            cycle_values = ["Todos"] + [str(cycle[0]) for cycle in cycles]
            self.cycle_combobox['values'] = cycle_values
            self.cycle_combobox.set("Todos")
        except Exception as e:
            self.logger.error(f"Error al cargar ciclos: {e}")
            messagebox.showerror("Error", f"Error al cargar ciclos: {e}")
        finally:
            if self.crud:
                self.crud.close()
                self.crud = None
    
    def on_cycle_selected(self, event):
        """Maneja el evento de selección de ciclo."""
        try:
            selected = self.cycle_combobox.get()
            self.selected_cycle = None if selected == "Todos" else selected
            self.load_data()
        except Exception as e:
            self.logger.error(f"Error al seleccionar ciclo: {e}")
            messagebox.showerror("Error", f"Error al seleccionar ciclo: {e}")