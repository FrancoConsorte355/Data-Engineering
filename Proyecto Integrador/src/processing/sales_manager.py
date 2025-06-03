import os
import shutil
from typing import List
import pandas as pd
from datetime import datetime, time
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
        - Convierte la columna SalesDate de string a datetime.time para tipo TIME.
        """
        for _, row in df.iterrows():
            raw = row.get('SalesDate')
            if pd.isna(raw) or raw is None:
                sales_date = None
            else:
                # Si ya es datetime.time, mantenerlo
                if isinstance(raw, time):
                    sales_date = raw
                else:
                    # Intentar parsear formato mm:ss.S o HH:MM:SS
                    try:
                        sales_date = datetime.strptime(str(raw), '%M:%S.%f').time()
                    except ValueError:
                        try:
                            sales_date = datetime.strptime(str(raw), '%H:%M:%S').time()
                        except ValueError:
                            # Fallback: guardar como None o lanzar error
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
                TransactionNumber=str(row['TransactionNumber'])
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
        Ahora lee el CSV sin parsear fechas, para manejar tiempo puro.
        """
        for ruta in rutas:
            df = pd.read_csv(ruta, dtype=str)  # Leer todo como str
            # Convertir columnas numéricas a sus tipos
            df['SalesID']         = df['SalesID'].astype(int)
            df['SalesPersonID']   = df['SalesPersonID'].astype(int)
            df['CustomerID']      = df['CustomerID'].astype(int)
            df['ProductID']       = df['ProductID'].astype(int)
            df['Quantity']        = df['Quantity'].astype(float)
            df['Discount']        = df['Discount'].astype(float)
            df['TotalPrice']      = df['TotalPrice'].astype(float)
            # SalesDate permanece como cadena hasta procesar
            # TransactionNumber ya es str

            self.procesar_dataframe(df)
            self.marcar_procesado(ruta)
