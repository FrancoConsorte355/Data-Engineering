# src/reports/pandas_status_report.py
import pandas as pd
from src.domain.log import Log

class PandasStatusReport:
    """
    Genera informes tabulares usando pandas.

    - Convierte una lista de objetos Log en un DataFrame
    - Utiliza groupby y agg para calcular conteos y métricas por sala
    - Proporciona métodos para exportar a CSV o Excel
    """
    def __init__(self):
        # Define aggregation functions for fields
        self.agg_funcs = {
            'temperatura':[ 'mean', 'max', 'min'],
            'humedad':    ['mean', 'max', 'min'],
            'co2':        ['mean', 'max', 'min']
        }

    def generate(self, records: list[Log]) -> pd.DataFrame:
        # Transform Log objects to DataFrame
        df = pd.DataFrame([vars(r) for r in records])              #Convierte una lista de objetos en una lista de diccionarios con sus atributos.
        # Group by sala and aggregate
        grouped = df.groupby('sala').agg(self.agg_funcs)
        # Flatten MultiIndex columns
        grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]
        return grouped.reset_index()

    def export_csv(self, df: pd.DataFrame, path: str):
        df.to_csv(path, index=False)

    def export_excel(self, df: pd.DataFrame, path: str):
        df.to_excel(path, index=False)