import os
import sys
from typing import List

def setup_environment() -> None:
    """
    Configura el entorno de ejecución estableciendo las rutas necesarias
    para los imports usando las carpetas existentes.
    """
    try:
        # Obtener el directorio actual donde está el main.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Directorio actual: {current_dir}")
        
        # Agregar el directorio actual al path
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
            
        # Verificar dónde está el config_manager
        if os.path.exists(os.path.join(current_dir, 'config_manager.py')):
            # Si está en el directorio actual, ya está en el path
            pass
        else:
            # Buscar en otros directorios comunes
            possible_config_locations = [
                os.path.join(current_dir, 'config'),
                os.path.join(current_dir, 'Interfaces'),
                os.path.join(current_dir, 'utils')
            ]
            
            for location in possible_config_locations:
                if os.path.exists(os.path.join(location, 'config_manager.py')):
                    if location not in sys.path:
                        sys.path.append(location)
                    break
                    
        # print("\nRutas configuradas en sys.path:")
        # for path in sys.path:
        #     print(f"- {path}")
                
    except Exception as e:
        print(f"Error al configurar el entorno: {str(e)}")
        sys.exit(1)

def main() -> None:
    """
    Función principal que inicia la aplicación.
    """
    try:
        # Configurar el entorno antes de importar MenuPrincipal
        setup_environment()
        
        try:
            # Intentar importar config_manager primero
            from config.config_manager import ConfigManager
            print("ConfigManager importado correctamente")
        except ImportError as e:
            print(f"Error al importar ConfigManager: {str(e)}")
            print("Asegúrate de que config_manager.py existe en alguna de las rutas del sistema")
            sys.exit(1)
        
        try:
            # Intentar importar MenuPrincipal
            from Inicio.menu_principal import MenuPrincipal
            print("MenuPrincipal importado correctamente")
        except ImportError as e:
            print(f"Error al importar MenuPrincipal: {str(e)}")
            print("Asegúrate de que menu_principal.py existe en alguna de las rutas del sistema")
            sys.exit(1)
        
        # Iniciar la aplicación
        app = MenuPrincipal()
        app.run()
        
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        sys.exit(1)

if __name__ == "__main__":
    main()