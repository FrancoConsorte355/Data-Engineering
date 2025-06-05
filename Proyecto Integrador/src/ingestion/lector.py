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
        try:
            os.makedirs(self._folder, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"Error al crear/verificar la carpeta '{self._folder}': {e}")

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
        try:
            archivos = []
            for nombre in os.listdir(self._folder):
                if nombre.lower().endswith('.csv'):
                    ruta = os.path.join(self._folder, nombre)
                    archivos.append(ruta)
            return archivos
        except FileNotFoundError:
            raise FileNotFoundError(f"La carpeta '{self._folder}' no existe.")
        except PermissionError:
            raise PermissionError(f"No tiene permiso para leer la carpeta '{self._folder}'.")
        except Exception as e:
            raise RuntimeError(f"Error inesperado al listar archivos CSV en '{self._folder}': {e}")

    def cargar(self, ruta: str) -> pd.DataFrame:
        if not os.path.isfile(ruta):
            raise FileNotFoundError(f"El archivo CSV '{ruta}' no existe.")
        if not ruta.lower().endswith('.csv'):
            raise ValueError(f"Extensión inválida para LectorCSV: '{ruta}'. Se esperaba un archivo .csv")

        try:
            df = pd.read_csv(ruta)
        except pd.errors.EmptyDataError:
            raise ValueError(f"El archivo CSV '{ruta}' está vacío.")
        except pd.errors.ParserError as pe:
            raise ValueError(f"Error al parsear el CSV '{ruta}': {pe}")
        except PermissionError:
            raise PermissionError(f"No tiene permiso para leer el archivo '{ruta}'.")
        except Exception as e:
            raise RuntimeError(f"Error inesperado al cargar CSV '{ruta}': {e}")

        # Si existe columna 'fecha', convertimos a datetime de forma segura
        if 'fecha' in df.columns:
            try:
                df['fecha'] = pd.to_datetime(df['fecha'], errors='ignore')
            except Exception as e:
                # No interrumpe la carga, solo se avisa
                print(f"⚠️ Advertencia: no se pudo convertir 'fecha' a datetime en '{ruta}': {e}")

        return df


class LectorJSON(LectorDatos):
    """
    Lector concreto para archivos JSON genéricos.
    """
    def listar_archivos(self) -> List[str]:
        try:
            archivos = []
            for nombre in os.listdir(self._folder):
                if nombre.lower().endswith('.json'):
                    ruta = os.path.join(self._folder, nombre)
                    archivos.append(ruta)
            return archivos
        except FileNotFoundError:
            raise FileNotFoundError(f"La carpeta '{self._folder}' no existe.")
        except PermissionError:
            raise PermissionError(f"No tiene permiso para leer la carpeta '{self._folder}'.")
        except Exception as e:
            raise RuntimeError(f"Error inesperado al listar archivos JSON en '{self._folder}': {e}")

    def cargar(self, ruta: str) -> pd.DataFrame:
        if not os.path.isfile(ruta):
            raise FileNotFoundError(f"El archivo JSON '{ruta}' no existe.")
        if not ruta.lower().endswith('.json'):
            raise ValueError(f"Extensión inválida para LectorJSON: '{ruta}'. Se esperaba un archivo .json")

        try:
            df = pd.read_json(ruta)
        except ValueError as ve:
            raise ValueError(f"Error al parsear el JSON '{ruta}': {ve}")
        except PermissionError:
            raise PermissionError(f"No tiene permiso para leer el archivo '{ruta}'.")
        except Exception as e:
            raise RuntimeError(f"Error inesperado al cargar JSON '{ruta}': {e}")

        # Si existe columna 'fecha', convertimos a datetime de forma segura
        if 'fecha' in df.columns:
            try:
                df['fecha'] = pd.to_datetime(df['fecha'], errors='ignore')
            except Exception as e:
                # No interrumpe la carga, solo se avisa
                print(f"⚠️ Advertencia: no se pudo convertir 'fecha' a datetime en '{ruta}': {e}")

        return df


class LectorFactory:
    """
    Factory Method para crear el lector adecuado según la extensión.
    """
    @staticmethod
    def get_lector(ext: str) -> LectorDatos:
        if not isinstance(ext, str) or len(ext) == 0:
            raise ValueError("La extensión proporcionada no es válida.")
        ext = ext.lower()
        if ext == '.csv':
            return LectorCSV()
        if ext == '.json':
            return LectorJSON()
        raise ValueError(f"Formato no soportado: '{ext}'. Solo se aceptan .csv o .json")
