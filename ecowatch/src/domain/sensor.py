# src/domain/sensor.py
from dataclasses import dataclass

@dataclass
class Sensor:
    name: str
    unit: str
