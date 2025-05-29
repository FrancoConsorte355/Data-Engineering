# test_db_connection.py

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from src.db import engine, SessionLocal

def main():
    session = None
    try:
        # 1) Probar engine directo
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Engine OK. SELECT 1 →", result.scalar())

        # 2) Probar sesión ORM
        session = SessionLocal()
        result2 = session.execute(text("SELECT 1"))
        print("✅ Session ORM OK. SELECT 1 →", result2.scalar())

    except SQLAlchemyError as e:
        print("❌ Falló la conexión:", e)

    finally:
        if session:
            session.close()

if __name__ == "__main__":
    main()
