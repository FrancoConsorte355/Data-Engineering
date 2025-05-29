# src/ingestion/validators.py
from datetime import datetime  # Importa la clase datetime para trabajar con fechas y horas
from src.domain.log import Log  # Importa la clase Log, que representa un registro validado

class Validator:  # Define la clase Validator, que contiene métodos de validación
    @staticmethod
    def validate(record: dict) -> Log:  # Método estático que valida un diccionario y retorna un Log
        # timestamp
        ts = record.get('timestamp')  # Obtiene el valor de 'timestamp' del diccionario
        try:
            ts_dt = datetime.fromisoformat(ts)  # Intenta convertir el timestamp a un objeto datetime
        except Exception as e:
            raise ValueError(f"Invalid timestamp: {ts}") from e  # Si falla, lanza un error indicando que el timestamp es inválido

        # numeric
        try:
            temp = float(record.get('temperatura'))  # Convierte 'temperatura' a float
            hum = float(record.get('humedad'))       # Convierte 'humedad' a float
            co2 = float(record.get('co2'))           # Convierte 'co2' a float
        except Exception:
            raise ValueError("Invalid numeric fields")  # Si alguna conversión falla, lanza un error

        # estado
        estado = record.get('estado')  # Obtiene el valor de 'estado'
        if estado not in ('INFO', 'WARN', 'ERROR'):  # Verifica que 'estado' sea uno de los valores permitidos
            raise ValueError(f"Invalid estado: {estado}")  # Si no, lanza un error

        # mensaje
        msg = record.get('mensaje', '')  # Obtiene 'mensaje', o una cadena vacía si no existe

        # sala
        sala = record.get('sala')  # Obtiene el valor de 'sala'

        return Log(  # Crea y retorna un objeto Log con los valores validados
            timestamp=ts_dt,
            sala=sala,
            estado=estado,
            temperatura=temp,
            humedad=hum,
            co2=co2,
            mensaje=msg
        )