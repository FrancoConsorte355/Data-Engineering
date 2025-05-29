# src/reports/base.py
from abc import ABC, abstractmethod

class Report(ABC):
    """
   Clase base para todos los reportes.
    """
    @abstractmethod
    def generate(self, records: list) -> any:
        """procesa record y retorna data."""
        pass