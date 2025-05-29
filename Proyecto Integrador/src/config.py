# src/config.py
"""
Configuraciones de entorno para el proyecto.
Se leen variables desde el fichero .env mediante python-decouple.
"""
from decouple import config
import os

# -- Rutas de datos --
# Carpeta donde están los CSV/JSON de diario
DATA_DIR = config('DATA_DIR', default=os.path.join(os.getcwd(), 'data', 'diarios'))
# Carpeta donde se moverán los archivos procesados
PROCESSED_DIR = config('PROCESSED_DIR', default=os.path.join(os.getcwd(), 'data', 'procesados'))

# -- Credenciales de Base de Datos MySQL --
DB_HOST     = config('DB_HOST',     default='localhost')
DB_PORT     = config('DB_PORT',     cast=int, default=3306)
DB_USER     = config('DB_USER',     default='root')
DB_PASSWORD = config('DB_PASSWORD', default='')
DB_NAME     = config('DB_NAME',     default='')

# URL de conexión para SQLAlchemy (MySQL + mysqlconnector)
DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

