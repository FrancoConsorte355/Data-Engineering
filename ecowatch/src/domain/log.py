# src/domain/log.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Log:
    timestamp: datetime
    sala: str
    estado: str
    temperatura: float
    humedad: float
    co2: float
    mensaje: str