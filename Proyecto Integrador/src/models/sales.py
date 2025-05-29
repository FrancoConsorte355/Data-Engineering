# src/models/sales.py
from sqlalchemy import Column, Integer, Float, String
from src.db import Base

class Sales(Base):
    __tablename__ = 'sales'

    SalesID = Column('SalesID', Integer, primary_key=True)
    SalesPersonID = Column('SalesPersonID', Integer, nullable=False)
    CustomerID = Column('CustomerID', Integer, nullable=False)
    ProductID = Column('ProductID', Integer, nullable=False)
    Quantity = Column('Quantity', Float, nullable=False)
    Discount = Column('Discount', Float, default=0.0)
    TotalPrice = Column('TotalPrice', Float, nullable=False)
    SalesDate = Column('SalesDate', String(20), nullable=False)  # Cambiado a String para aceptar valores como '31:24.2'
    TransactionNumber = Column('TransactionNumber', String(100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<Sales id={self.SalesID} salesDate={self.SalesDate} total={self.TotalPrice:.2f} transaction={self.TransactionNumber}>"
        )

    def calcular_total(self) -> float:
        """
        Reusa el campo TotalPrice almacenado.
        """
        return self.TotalPrice


