import tkinter as tk
import sys
import logging
import os

# Agregar el directorio raíz al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from generar_listas.src.components import GeneradorAsistencia

def main():
    # Configurar logging
    logging.basicConfig( 
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    try:
        # Crear la ventana raíz
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana raíz
        
        # Iniciar el generador de asistencia
        app = GeneradorAsistencia(root)
        app.run()
        
        # Iniciar el loop principal
        root.mainloop()
    except Exception as e:
        logging.error(f"Error en la ejecución principal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()