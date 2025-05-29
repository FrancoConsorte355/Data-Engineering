# src/models/producto.py
from abc import ABC, abstractmethod
from typing import Any, Dict

class PriceStrategy(ABC):
    """
    Strategy pattern: define interface para distintos cálculos de precio.
    """
    @abstractmethod
    def calcular(self, Price: float, Quantity: float) -> float:
        """Calcula el importe total según la estrategia concreta."""
        pass

class PriceNormal(PriceStrategy):
    """
    Estrategia por defecto: precio_unitario * cantidad.
    """
    def calcular(self, Price: float, Quantity: float) -> float:
        return Price * Quantity

class PriceDescount(PriceStrategy):
    """
    Estrategia de precio con descuento porcentual.
    """
    def __init__(self, discount: float) -> None:
        # descuento entre 0.0 y 1.0 (por ejemplo 0.10 para 10%)
        if not (0 <= discount <= 1):
            raise ValueError("Descuento debe estar entre 0 y 1.")
        self._discount = discount

    def calcular(self, Price: float, Quantity: float) -> float:
        subtotal = Price * Quantity
        return subtotal * (1 - self._discount)

# Aquí se pueden añadir nuevas estrategias: Producto
# class PrecioConImpuesto(PriceStrategy): ...

class Products:
    """
    Entidad Producto:
    - Single Responsibility: almacena atributos y delega cálculo de importe a una estrategia.
    - Strategy: permite cambiar cálculo de total sin modificar la clase.
    """
    def __init__(
        self,
        ProductID: int,
        ProductName: str,
        Price: float,
        CategoryID: int,
        Class: str,
        ModifyDate: str,
        Resistant: str,
        IsAllergic: bool,
        VitalityDays: int,
        strategy: PriceStrategy = None
    ) -> None:
        self._ProductID = ProductID
        self._ProductName = ProductName
        self._Price = Price
        # Si no se provee estrategia, usar la normal, es una forma resumida de hacer un if/else
        self._strategy = strategy or PriceNormal()

    @property
    def ProductID(self) -> int:
        """Devuelve el identificador del producto"""
        return self._ProductID

    @property
    def ProductName(self) -> str:
        """Devuelve el nombre del producto"""
        return self._ProductName

    @property
    def Price(self) -> float:
        """Devuelve el precio unitario del producto"""
        return self._Price
    
    @property
    def CategoryID(self) -> int:
        """Devuelve el identificador de la categoría del producto"""
        return self._CategoryID
    
    @property
    def Class(self) -> str:
        """Devuelve la clase del producto"""
        return self._Class
    
    @property
    def ModifyDate(self) -> str:
        """Devuelve la fecha de modificación del producto"""
        return self._ModifyDate
    
    @property
    def Resistant(self) -> str:
        """Devuelve la resistencia del producto"""
        return self._Resistant
    
    @property
    def IsAllergic(self) -> bool:
        """Devuelve si el producto es alérgico"""
        return self._IsAllergic
    
    @property
    def VitalityDays(self) -> int:
        """Devuelve los días de vitalidad del producto"""
        return self._VitalityDays
    

    def calcular_total(self, Quantity: float) -> float:
        """
        Calcula el importe total delegando a la estrategia configurada.
        """
        return self._strategy.calcular(self._Price, Quantity)

    def __repr__(self) -> str:
        """Representación para depuración"""
        return (
            f"<ProductID id={self._id} ProductName={self.ProductName} "
            f"Price={self._Price}>"
        )

class ProductoFactory:
    """
    Factory Method: crea instancias de Producto aplicando la estrategia adecuada
    según la información del diccionario de datos.

    from_dict:
    - **data: Dict[str, Any]**: indica que `data` debe ser un diccionario cuyas claves son strings y cuyos valores pueden ser de cualquier tipo.
    - **-> Producto**: significa que este método devuelve un objeto de la clase `Producto`.
    """
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Products:
        # data: Dict[str, Any]  <- `data` es un dict con claves str y valores de cualquier tipo
        # -> Producto         <- este método retorna un objeto `Producto`
        id_ = int(data.get('ProductID', 0))
        ProductName = data.get('ProductName', '')
        Price = float(data.get('Price', 0.0))
        # Obtener descuento si está presente; 0 si no existe o es None
        desc_raw = data.get('discount', 0) or 0
        try:
            discount = float(desc_raw)
        except (TypeError, ValueError):
            discount = 0.0
        # Seleccionar estrategia según valor de descuento
        if discount > 0:
            strategy = PriceDescount(discount)
        else:
            strategy = PriceNormal()
        # Crear y devolver el Producto con la estrategia elegida
        return Products(
            ProductID=id_,
            ProductName=ProductName,
            Price=Price,
            strategy=strategy
        )
