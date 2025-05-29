import os
import shutil
from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from src.models.sales import Sales

class SalesManager:
    """
    Clase gestora de ventas:
    - Recibe DataFrames de ventas validados.
    - Mapea filas a objetos de dominio Sales.
    - Persiste entidades en la base de datos usando SQLAlchemy.
    - Mueve CSV procesados a carpeta de archivado.
    """
    def __init__(
        self,
        db_session: Session,
        processed_dir: str = os.path.join(os.getcwd(), 'data', 'procesados')
    ) -> None:
        # Sesión de SQLAlchemy para transacciones
        self._session = db_session
        # Carpeta destino para CSV ya procesados
        self._processed_dir = processed_dir
        os.makedirs(self._processed_dir, exist_ok=True)

    def procesar_dataframe(self, df: pd.DataFrame) -> None:
        """
        Procesa un DataFrame de ventas:
        - Itera cada fila, crea instancia de Sales y la añade a la sesión.
        Maneja valores NaN en SalesDate convirtiéndolos a None para evitar errores de columna "nan".
        """
        for _, row in df.iterrows():
            # Convertir NaN de SalesDate a None para SQLAlchemy
            sales_date = row.get('SalesDate')
            if pd.isna(sales_date):
                sales_date = None

            sale = Sales(
                SalesID=int(row['SalesID']),
                SalesPersonID=int(row['SalesPersonID']),
                CustomerID=int(row['CustomerID']),
                ProductID=int(row['ProductID']),
                Quantity=float(row['Quantity']),
                Discount=float(row['Discount']),
                TotalPrice=float(row['TotalPrice']),
                SalesDate=sales_date,
                TransactionNumber=row['TransactionNumber']
            )
            self._session.add(sale)

    def marcar_procesado(self, ruta_csv: str) -> None:
        """
        Mueve el CSV procesado a la carpeta de procesados.
        """
        nombre = os.path.basename(ruta_csv)
        destino = os.path.join(self._processed_dir, nombre)
        shutil.move(ruta_csv, destino)

    def procesar_archivos(self, rutas: List[str]) -> None:
        """
        Conveniencia: procesa una lista de rutas de CSV.
        """
        for ruta in rutas:
            # Leer CSV, parseando la columna SalesDate si existe
            df = pd.read_csv(ruta, parse_dates=['SalesDate'])
            self.procesar_dataframe(df)
            self.marcar_procesado(ruta)
