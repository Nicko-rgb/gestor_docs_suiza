import tkinter as tk
import sys
import logging
from src.components import GeneradorAsistencia

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