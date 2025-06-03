# src/db.py

import pandas as pd
from decouple import config
from sqlalchemy import create_engine, text
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
            echo=False,       # Cambiar a True para ver el SQL generado en consola
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
        Devuelve un generador para un contexto de sesión de BD.
        Uso:
            sess_gen = db.get_session()
            session = next(sess_gen)       # abre la sesión
            ...  # usar session.execute(), session.add(), etc.
            try:
                next(sess_gen)             # cierra la sesión al terminar
            except StopIteration:
                pass
        """
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def run_sql(self, sql: str, params: dict = None) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL SELECT y devuelve un DataFrame de pandas.

        :param sql: Consulta SELECT a ejecutar.
        :param params: Diccionario de parámetros (ej. {'id': 5}) para la query.
        :return: pd.DataFrame con los resultados.
        """
        with self.engine.connect() as conn:
            df = pd.read_sql_query(text(sql), conn, params=params or {})
        return df

    def execute_sql(self, sql: str, params: dict = None) -> None:
        """
        Ejecuta un comando SQL de tipo DDL o DML (CREATE, INSERT, UPDATE, DELETE,
        CALL de procedimientos almacenados, creación de índices o triggers).
        No devuelve resultados; hace commit automáticamente si modifica datos.

        :param sql: Sentencia SQL a ejecutar (puede ser CREATE PROCEDURE, CALL, CREATE INDEX, etc.).
        :param params: Diccionario de parámetros para la sentencia.
        """
        with self.engine.connect() as conn:
            with conn.begin():  # comienza transacción y hace commit si no hay error
                conn.execute(text(sql), params or {})

# Instancia global única
db = Database()

# Exponer directamente los componentes más usados
engine       = db.engine
SessionLocal = db.SessionLocal
Base         = db.Base
get_session  = db.get_session

# Función para ejecutar SELECT y obtener DataFrame
def run_sql(sql: str, params: dict = None) -> pd.DataFrame:
    return db.run_sql(sql, params)

# Función para ejecutar DDL/DML sin retorno (procedimientos, triggers, índices, inserciones, etc.)
def execute_sql(sql: str, params: dict = None) -> None:
    db.execute_sql(sql, params)



