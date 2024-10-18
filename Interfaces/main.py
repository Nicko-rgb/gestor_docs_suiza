import os
import sys

# Obtener el directorio raíz del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))

# Agregar los directorios necesarios al path de Python
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'gestor_docs_suiza'))
sys.path.append(os.path.join(root_dir, 'gestor_docs_suiza', 'Interfaces'))

# Importar la clase MenuPrincipal
from Inicio.menu_principal import MenuPrincipal

if __name__ == "__main__":
    menu_principal = MenuPrincipal()
    menu_principal.run()