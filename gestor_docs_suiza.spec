# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Definir todos los archivos necesarios
added_files = [
    ('Interfaces/Plantillas/*', 'Plantillas'),
    ('Imagenes/*', 'Imagenes'),
    ('Interfaces/generar_listas/src/*.py', 'generar_listas/src'),
    ('Interfaces/Generador_Docs/src/*.py', 'Generador_Docs/src'),
    ('Interfaces/Excel_a_Sql/*.py', 'Excel_a_Sql'),
    ('Interfaces/config/*.py', 'config'),
    ('Interfaces/Crud/*.py', 'Crud'),
    ('Interfaces/Inicio/*.py', 'Inicio'),
    ('Interfaces/config/*', 'config.json')
]

a = Analysis(
    ['Interfaces/main.py'],
    pathex=['.', './Interfaces'],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'generar_listas',
        'generar_listas.src',
        'generar_listas.src.components',
        'generar_listas.src.base_components',
        'generar_listas.src.config',
        'generar_listas.src.db_manager',
        'generar_listas.src.document',
        'generar_listas.src.styles',
        'Generador_Docs.src.document_generator',
        'Excel_a_Sql.excel_sql_id',
        'Inicio.menu_principal',
        'config.config_manager',
        'config.config.json'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,        # Incluido para one-file
    a.zipfiles,        # Incluido para one-file
    a.datas,           # Incluido para one-file
    [],
    name='Gestor de Documentos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,     # Cambiado a False para ocultar la consola
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Imagenes\\icono_principal.ico',
)