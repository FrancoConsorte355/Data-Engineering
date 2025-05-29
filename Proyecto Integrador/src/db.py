# src/db.py

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1) Carga de credenciales desde el .env
DB_HOST     = config('DB_HOST')
DB_PORT     = config('DB_PORT', cast=int)
DB_USER     = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_NAME     = config('DB_NAME')

# 2) Construcción del URL de conexión
#    mysql+mysqlconnector://<usuario>:<pwd>@<host>:<puerto>/<base>
DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# 3) Creación del Engine
#    future=True activa la API 2.0 de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,       # pon True si quieres ver los SQL generados
    future=True,
    pool_pre_ping=True
)

# 4) SessionLocal es la fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True
)

# 5) Base para tus modelos declarativos
Base = declarative_base()

def get_session():
    """
    Devuelve una nueva sesión de BD.
    Úsala así:

        with get_session() as session:
            # ... tu código ...
    """
    session = SessionLocal()           
    try:
        yield session
    finally:
        session.close()

