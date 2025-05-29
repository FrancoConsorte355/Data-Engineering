# src/ingestion/lector.py
import os
from abc import ABC, abstractmethod
from typing import List
import pandas as pd

from src.config import DATA_DIR


class LectorDatos(ABC):
    """
    Interfaz (Strategy) para lectores de datos de diferentes formatos.
    Define los métodos que cada lector debe implementar.
    """
    def __init__(self, carpeta: str = DATA_DIR) -> None:
        # Carpeta donde buscar archivos de datos (CSV o JSON)
        self._folder = carpeta
        os.makedirs(self._folder, exist_ok=True)

    @abstractmethod
    def listar_archivos(self) -> List[str]:
        """
        Lista rutas a archivos del formato correspondiente.
        """
        pass

    @abstractmethod
    def cargar(self, ruta: str) -> pd.DataFrame:
        """
        Carga un archivo en un DataFrame sin validaciones de esquema.
        """
        pass


class LectorCSV(LectorDatos):
    """
    Lector concreto para archivos CSV genéricos.
    """
    def listar_archivos(self) -> List[str]:
        return [
            os.path.join(self._folder, f)
            for f in os.listdir(self._folder)
            if f.lower().endswith('.csv')
        ]

    def cargar(self, ruta: str) -> pd.DataFrame:
        # Lee cualquier CSV sin exigir columnas específicas
        df = pd.read_csv(ruta)
        # Si existe columna 'fecha', convertimos a datetime de forma segura
        #if 'fecha' in df.columns:
        #   df['fecha'] = pd.to_datetime(df['fecha'], errors='ignore')
        return df


class LectorJSON(LectorDatos):
    """
    Lector concreto para archivos JSON genéricos.
    """
    def listar_archivos(self) -> List[str]:
        return [
            os.path.join(self._folder, f)
            for f in os.listdir(self._folder)
            if f.lower().endswith('.json')
        ]

    def cargar(self, ruta: str) -> pd.DataFrame:
        # Lee cualquier JSON asumiendo lista de registros o dict de listas
        df = pd.read_json(ruta)
        # Si existe columna 'fecha', convertimos a datetime
        #if 'fecha' in df.columns:
        #    df['fecha'] = pd.to_datetime(df['fecha'], errors='ignore')
        return df


class LectorFactory:
    """
    Factory Method para crear el lector adecuado según la extensión.
    """
    @staticmethod
    def get_lector(ext: str) -> LectorDatos:
        ext = ext.lower()
        if ext == '.csv':
            return LectorCSV()
        if ext == '.json':
            return LectorJSON()
        raise ValueError(f"Formato no soportado: {ext}")