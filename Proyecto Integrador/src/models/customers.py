class Customer:
    def __init__(
                 self,
                 CustomerID: int,
                 FirstName: str,
                 MiddleInitial: str,
                 CityID: int,
                 Address: str,
                             ) -> None:
        """ Entidad Cliente:
            Single Responsibility: almacena atributos del cliente.
        """
        self._CustomerID = CustomerID
        self._FirstName = FirstName
        self._MiddleInitial = MiddleInitial
        self._CityID = CityID
        self._Address = Address

    @property                                           ## Propiedades para acceder a los atributos privados
                                                        ## Se utilizan para encapsular los atributos y permitir su acceso de forma controlada
    def CustomerID(self) -> int:
        """Devuelve el identificador del cliente"""
        return self._CustomerID
    
    @property
    def FirstName(self) -> str:
        """Devuelve el nombre del cliente"""
        return self._FirstName
    
    @property
    def MiddleInitial(self) -> str:
        """Devuelve la inicial del segundo nombre del cliente"""
        return self._MiddleInitial
    
    @property
    def CityID(self) -> int:
        """Devuelve el identificador de la ciudad del cliente"""
        return self._CityID
    
    @property
    def Address(self) -> str:
        """Devuelve la dirección del cliente"""
        return self._Address
    
    def __repr__(self) -> str:
        """Representación legible del objeto para depuración"""
        return f"<Cliente CustomerID={self._CustomerID} FirstName={self._FirstName} MiddleInitial={self._MiddleInitial} CityID={self._CityID} Address={self._Address}>"
    