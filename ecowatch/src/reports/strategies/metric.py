# src/reports/strategies/metric.py
from abc import ABC, abstractmethod

class MetricStrategy(ABC):
    """
    Strategy interface for computing a metric over a list of Log entries.
    """
    @property
    @abstractmethod
    def metric_name(self) -> str:
        pass

    @property
    @abstractmethod
    def field_name(self) -> str:
        pass

    @abstractmethod
    def compute(self, logs: list) -> float:
        pass

class AvgStrategy(MetricStrategy):
    def __init__(self, field_name: str):
        self._field = field_name

    @property
    def metric_name(self) -> str:
        return 'avg'

    @property
    def field_name(self) -> str:
        return self._field

    def compute(self, logs: list) -> float:
        values = [getattr(log, self._field) for log in logs]
        return sum(values) / len(values) if values else 0.0

class MaxStrategy(MetricStrategy):
    def __init__(self, field_name: str):
        self._field = field_name

    @property
    def metric_name(self) -> str:
        return 'max'

    @property
    def field_name(self) -> str:
        return self._field

    def compute(self, logs: list) -> float:
        values = [getattr(log, self._field) for log in logs]
        return max(values) if values else 0.0

class MinStrategy(MetricStrategy):
    def __init__(self, field_name: str):
        self._field = field_name

    @property
    def metric_name(self) -> str:
        return 'min'

    @property
    def field_name(self) -> str:
        return self._field

    def compute(self, logs: list) -> float:
        values = [getattr(log, self._field) for log in logs]
        return min(values) if values else 0.0