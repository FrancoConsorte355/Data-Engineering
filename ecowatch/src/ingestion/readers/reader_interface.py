# src/ingestion/readers/base.py
from abc import ABC, abstractmethod

class ReaderInterface(ABC):
    @abstractmethod
    def read_logs(self):
        """Yields each log record as a dict."""
        raise NotImplementedError
    
    #Este archivo define una interfaz abstracta para lectores de logs.
    #Obliga a que cualquier clase que herede de ReaderInterface implemente el método read_logs, que debe devolver los registros de log como diccionarios. 
    #Esto ayuda a mantener una estructura consistente y facilita la extensión del código.