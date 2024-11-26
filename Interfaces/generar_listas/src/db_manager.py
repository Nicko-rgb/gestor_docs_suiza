# db_manager.py
import mysql.connector
import logging
from tkinter import messagebox
from typing import List, Tuple, Optional
from src.config import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
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