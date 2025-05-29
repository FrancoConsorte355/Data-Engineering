class Employee:
    def __init__(self, EmployeeID: int, FirstName: str, MiddleInitial: str, LastName: str, BirthDate: str)-> None:
        """ Entidad Empleado:
            Single Responsibility: almacena atributos del empleado.
        """
        self._EmployeeID = EmployeeID
        self._FirstName = FirstName
        self._MiddleInitial = MiddleInitial
        self._LastName = LastName
        self._BirthDate = BirthDate

    @property
    def EmployeeID(self) -> int:
        """Devuelve el identificador del empleado"""
        return self._EmployeeID
    
    @property
    def FirstName(self) -> str:
        """Devuelve el nombre del empleado"""
        return self._FirstName
    
    @property
    def MiddleInitial(self) -> str:
        """Devuelve la inicial del segundo nombre del empleado"""
        return self._MiddleInitial
    
    @property
    def LastName(self) -> str:
        """Devuelve el apellido del empleado"""
        return self._LastName
    
    @property
    def BirthDate(self) -> str:
        """Devuelve la fecha de nacimiento del empleado"""
        return self._BirthDate

