import mysql.connector
from Crud.Config import DB_CONFIG

class Crud:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.cursor = None
        self.selected_cycle = None  # Añadimos el atributo selected_cycle
        self.connect()

    def connect(self):
        """Establece la conexión a la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database']
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as error:
            print(f"Error al conectar a la base de datos: {error}")
            raise

    def set_selected_cycle(self, cycle):
        """Establece el ciclo seleccionado"""
        self.selected_cycle = cycle

    def get_selected_cycle(self):
        """Obtiene el ciclo seleccionado actual"""
        return self.selected_cycle

    def fetch_all_students(self):
        try:
            if not self.connection.is_connected():
                self.connect()
            self.cursor.execute("SELECT * FROM estudiantes_del_dsi")
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"Error al obtener estudiantes: {error}")
            return []
        except Exception as e:
            print(f"Error inesperado: {e}")
            return []

    def fetch_all_cycles(self):
        try:
            if not self.connection.is_connected():
                self.connect()
            self.cursor.execute("SELECT DISTINCT ID_CICLO FROM estudiantes_del_dsi ORDER BY ID_CICLO")
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"Error al obtener ciclos: {error}")
            return []
        except Exception as e:
            print(f"Error inesperado: {e}")
            return []

    def fetch_students_by_cycle(self, cycle):
        try:
            if not self.connection.is_connected():
                self.connect()
            query = "SELECT * FROM estudiantes_del_dsi WHERE ID_CICLO = %s ORDER BY ID_Estudiante"
            self.cursor.execute(query, (cycle,))
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"Error al obtener estudiantes por ciclo: {error}")
            return []
        except Exception as e:
            print(f"Error inesperado: {e}")
            return []

    def add_student(self, data):
        try:
            if not self.connection.is_connected():
                self.connect()
            query = """
                INSERT INTO estudiantes_del_dsi 
                (DNI, Nombre, Apellido_P, Apellido_M, Correo, Numero_telefono, Direccion, ID_Ciclo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                data['DNI'], data['Nombre'], data['Apellido P'], data['Apellido M'],
                data['Correo'], data['Número'], data['Dirección'], data['ID Ciclo']
            )
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Estudiante agregado correctamente.")
        except mysql.connector.Error as error:
            print(f"Error al agregar estudiante: {error}")
            self.connection.rollback()
            raise
        except Exception as e:
            print(f"Error inesperado: {e}")
            self.connection.rollback()
            raise

    def update_student(self, data):
        try:
            if not self.connection.is_connected():
                self.connect()
            query = """
                UPDATE estudiantes_del_dsi 
                SET DNI=%s, Nombre=%s, Apellido_P=%s, Apellido_M=%s, 
                    Correo=%s, Numero_telefono=%s, Direccion=%s, ID_CICLO=%s 
                WHERE ID_Estudiante=%s
            """
            values = (
                data['DNI'], data['Nombre'], data['Apellido P'], data['Apellido M'],
                data['Correo'], data['Número'], data['Dirección'], data['ID Ciclo'],
                data['ID']
            )
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Estudiante actualizado correctamente.")
        except mysql.connector.Error as error:
            print(f"Error al actualizar estudiante: {error}")
            self.connection.rollback()
            raise
        except Exception as e:
            print(f"Error inesperado: {e}")
            self.connection.rollback()
            raise

    def delete_student(self, student_id):
        try:
            if not self.connection.is_connected():
                self.connect()
            query = "DELETE FROM estudiantes_del_dsi WHERE ID_estudiante=%s"
            self.cursor.execute(query, (student_id,))
            self.connection.commit()
            print("Estudiante eliminado correctamente.")
        except mysql.connector.Error as error:
            print(f"Error al eliminar estudiante: {error}")
            self.connection.rollback()
            raise
        except Exception as e:
            print(f"Error inesperado: {e}")
            self.connection.rollback()
            raise

    def close(self):
        """Cerrar conexión y cursor de manera segura"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("Conexión a la base de datos cerrada")
        except mysql.connector.Error as error:
            print(f"Error al cerrar la conexión: {error}")
        except Exception as e:
            print(f"Error inesperado al cerrar la conexión: {e}")