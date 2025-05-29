class Category:
    def __init__(self, CategoryID: int, CategoryName: str) -> None:
        """ Entidad Categoría:
            Single Responsibility: almacena atributos de la categoría.
        """
        self._CategoryID = CategoryID
        self._CategoryName = CategoryName

    @property
    def CategoryID(self) -> int:
        """Devuelve el identificador de la categoría"""
        return self._CategoryID

    @property
    def CategoryName(self) -> str:
        """Devuelve el nombre de la categoría"""
        return self._CategoryName