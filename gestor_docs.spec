# gestor_docs.spec
import os
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

# Obtener la ruta absoluta del proyecto
base_path = os.path.abspath(os.getcwd())

# Función para crear rutas absolutas de los recursos
def resource_path(relative_path):
    return os.path.join(base_path, relative_path)

a = Analysis(
    ['Interfaces/main.py'],
    pathex=[base_path] + [
        resource_path('Interfaces'),
        resource_path('Interfaces/Crud'),
        resource_path('Interfaces/Excel_a_Sql'),
        resource_path('Interfaces/Generador_Docs'),
        resource_path('Interfaces/Generador_Docs/src'),
        resource_path('Interfaces/generar_listas'),
        resource_path('Interfaces/generar_listas/src'),
        resource_path('Interfaces/Inicio'),
    ],
    binaries=[],
    datas=[
        (resource_path('Imagenes'), 'Imagenes'),  # Asegura rutas absolutas
        (resource_path('Interfaces/Plantillas'), 'Plantillas'),
        (resource_path('Interfaces/Generador_Docs/src'), 'Generador_Docs/src'),
        (resource_path('Interfaces/generar_listas/src'), 'generar_listas/src'),
        (resource_path('Interfaces/Excel_a_Sql'), 'Excel_a_Sql'),
    ],
    hiddenimports=[
        'PIL',
        'PIL._tkinter_finder',  # Añadido para soporte de imágenes
        'Interfaces.Generador_Docs.src.document_generator',
        'Interfaces.generar_listas.src.components',
        'Interfaces.Excel_a_Sql.excel_sql_id',
        'Interfaces.Crud.main',
        'Interfaces.Inicio.main',
        'Interfaces.Generador_Docs.main',
        'Interfaces.generar_listas.main',
        'Interfaces.Excel_a_Sql.main',
        'pandas',
        'openpyxl',
        'tkinter',
        'tkinter.ttk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='gestor_docs',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Mantener True para ver errores
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=resource_path('Imagenes/logoDSI.ico') if os.path.exists(resource_path('Imagenes/logoDSI.ico')) else None,
)