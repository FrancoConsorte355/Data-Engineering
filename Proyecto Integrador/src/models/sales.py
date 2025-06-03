# src/models/sales.py
from sqlalchemy import Column, Integer, Float, String, Time
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
    SalesDate = Column('SalesDate', Time, nullable=False)
    TransactionNumber = Column('TransactionNumber', String(100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<Sales id={self.SalesID} salesDate={self.SalesDate} "
            f"total={self.TotalPrice:.2f} transaction={self.TransactionNumber}>"
        )

    def calcular_total(self) -> float:
        """
        Reusa el campo TotalPrice almacenado.
        """
        return self.TotalPrice

    @classmethod
    def builder(cls) -> 'SalesBuilder':
        """
        Inicia el builder para construir instancias de Sales.
        """
        return SalesBuilder()


class SalesBuilder:
    """
    Builder para Sales:
    Permite construir un objeto Sales paso a paso,
    añadiendo nuevos campos sin modificar la firma del constructor.
    """
    def __init__(self) -> None:
        self._values = {}

    def set_sales_id(self, sales_id: int) -> 'SalesBuilder':
        self._values['SalesID'] = sales_id
        return self

    def set_sales_person_id(self, sp_id: int) -> 'SalesBuilder':
        self._values['SalesPersonID'] = sp_id
        return self

    def set_customer_id(self, cust_id: int) -> 'SalesBuilder':
        self._values['CustomerID'] = cust_id
        return self

    def set_product_id(self, prod_id: int) -> 'SalesBuilder':
        self._values['ProductID'] = prod_id
        return self

    def set_quantity(self, qty: float) -> 'SalesBuilder':
        self._values['Quantity'] = qty
        return self

    def set_discount(self, discount: float) -> 'SalesBuilder':
        self._values['Discount'] = discount
        return self

    def set_total_price(self, total: float) -> 'SalesBuilder':
        self._values['TotalPrice'] = total
        return self

    def set_sales_date(self, sales_date: Time) -> 'SalesBuilder':
        self._values['SalesDate'] = sales_date
        return self

    def set_transaction_number(self, txn: str) -> 'SalesBuilder':
        self._values['TransactionNumber'] = txn
        return self

    def build(self) -> Sales:
        """
        Valida y construye la instancia de Sales.
        Lanza ValueError si faltan campos obligatorios.
        """
        required = [
            'SalesID', 'SalesPersonID', 'CustomerID', 'ProductID',
            'Quantity', 'Discount', 'TotalPrice', 'SalesDate', 'TransactionNumber'
        ]
        missing = [f for f in required if f not in self._values]
        if missing:
            raise ValueError(f"Faltan campos obligatorios para Sales: {missing}")
        return Sales(**self._values)

