class Cities:
    def __init__(
                 self,
                 CityID: int,
                 CityName: str,
                 Zipcode: int,
                 CountryID: int,
                    ) -> None:
        """ Entidad Ciudad:
            Single Responsibility: almacena atributos de la ciudad.
        """
        self._CityID = CityID
        self._CityName = CityName
        self._Zipcode = Zipcode
        self._CountryID = CountryID
    

@property
def CityID(self) -> int:
    """Devuelve el identificador de la ciudad"""
    return self._CityID

@property
def CityName(self) -> str:
    """Devuelve el nombre de la ciudad"""
    return self._CityName

@property
def Zipcode(self) -> int:
    """Devuelve el código postal de la ciudad"""
    return self._Zipcode

@property
def CountryID(self) -> int:
    """Devuelve el identificador del país de la ciudad"""
    return self._CountryID