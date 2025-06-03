# src/db.py
import pandas as pd
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Singleton para gestionar la conexión a la base de datos
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._setup()
        return cls._instance

    def _setup(self):
        # 1) Carga de credenciales desde .env
        host     = config('DB_HOST')
        port     = config('DB_PORT', cast=int)
        user     = config('DB_USER')
        password = config('DB_PASSWORD')
        name     = config('DB_NAME')

        # 2) Construcción de URL de conexión
        url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{name}"

        # 3) Creación del engine (único en toda la app)
        self.engine = create_engine(
            url,
            echo=False,       # True para ver SQL generado
            future=True,
            pool_pre_ping=True
        )

        # 4) Fábrica de sesiones, atada al mismo engine
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            future=True
        )

        # 5) Base declarativa para los modelos
        self.Base = declarative_base()

    def get_session(self):
        """
        Devuelve un contexto de sesión para usar con `with`:
            with db.get_session() as session:
                ...
        """
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def run_sql(self, sql: str, params: dict = None) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL SELECT y devuelve un DataFrame de pandas.

        :param sql: Consulta SQL a ejecutar.
        :param params: Diccionario de parámetros para la consulta.
        :return: pd.DataFrame con los resultados.
        """
        with self.engine.connect() as conn:
            df = pd.read_sql_query(sql, conn, params=params)
        return df

# Instancia global única
db = Database()

# Exponer directamente los componentes más usados
engine       = db.engine
SessionLocal = db.SessionLocal
Base         = db.Base
get_session  = db.get_session
# Método para ejecución de consultas y retorno en DataFrame
def run_sql(sql: str, params: dict = None) -> pd.DataFrame:
    return db.run_sql(sql, params)

