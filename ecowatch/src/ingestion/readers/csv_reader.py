# src/ingestion/readers/csv_reader.py

import csv                      # Importa el módulo csv para leer archivos CSV.
import time                     # Importa el módulo time para usar la función sleep.
from .reader_interface import ReaderInterface  # Importa la interfaz base desde el mismo paquete.
from ...config.settings import Settings        # Importa la configuración global desde tres niveles arriba.

class CsvReader(ReaderInterface):              # Define la clase CsvReader que hereda de ReaderInterface.
    def __init__(self, path=None, delay=Settings.STREAM_DELAY_SEC):  # Constructor con parámetros opcionales.
        self.path = path or Settings.LOG_CSV_PATH   # Usa el path dado o el path por defecto de Settings.
        self.delay = delay                         # Asigna el delay (retardo) para la lectura.

    def read_logs(self):                           # Método para leer los logs del archivo CSV.
        with open(self.path, newline='', encoding='utf-8') as f:  # Abre el archivo CSV con codificación UTF-8.
            reader = csv.DictReader(f)             # Crea un lector que convierte cada fila en un diccionario.
            for row in reader:                     # Itera sobre cada fila del archivo.
                yield row                          # Devuelve la fila como un diccionario (uno por uno).
                if self.delay:                     # Si hay retardo configurado...
                    time.sleep(self.delay)         # ...espera la cantidad de segundos indicada.