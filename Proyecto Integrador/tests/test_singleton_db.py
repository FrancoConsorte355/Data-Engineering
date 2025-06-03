# tests/test_singleton_db.py

import pytest
from src.db import Database, db

def test_database_instance_is_singleton():
    """
    Verifica que cada llamada a Database() devuelve la misma instancia.
    """
    inst1 = Database()
    inst2 = Database()
    assert inst1 is inst2, "Database() debería retornar siempre la misma instancia"

def test_db_proxy_is_same_as_new_instance():
    """
    Verifica que el proxy 'db' es la misma instancia que se obtiene al llamar a Database().
    """
    inst_new = Database()
    assert inst_new is db, "La instancia global 'db' debería ser idéntica a Database()"

def test_engine_is_same_object():
    """
    Asegura que todos los accesos a engine provienen de la misma conexión subyacente.
    """
    inst1 = Database()
    inst2 = Database()
    assert inst1.engine is inst2.engine, "El atributo 'engine' debe ser un único objeto compartido"

def test_sessionlocal_factory_is_same_object():
    """
    Asegura que SessionLocal es la misma fábrica de sesiones para todas las instancias.
    """
    inst1 = Database()
    inst2 = Database()
    assert inst1.SessionLocal is inst2.SessionLocal, "SessionLocal debe ser un único objeto compartido"
