class Country: 
    def __init__(self,CountryID: int, CountryName:str, CountryCode:str) -> None:
        """ Entidad País:
            Single Responsibility: almacena atributos del país.
        """
        self._CountryID = CountryID
        self._CountryName = CountryName
        self._CountryCode = CountryCode

    @property
    def CountryID(self) -> int:
        """Devuelve el identificador del país"""
        return self._CountryID

    @property
    def CountryName(self) -> str:
        """Devuelve el nombre del país"""
        return self._CountryName
    
    @property
    def CountryCode(self) -> str:
        """Devuelve el código del país"""
        return self._CountryCode
        