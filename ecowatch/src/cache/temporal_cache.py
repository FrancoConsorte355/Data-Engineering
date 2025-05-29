# src/cache/temporal_cache.py
from collections import deque  # Importa deque para una cola eficiente de doble extremo
from datetime import datetime, timedelta  # Importa datetime y timedelta para manejo de fechas

class TemporalCache:
    """
    Caché que mantiene registros dentro de una ventana de tiempo deslizante y maneja objetos Log.
    """
    def __init__(self, window_seconds=300, now_fn=None):
        # Define el tamaño de la ventana de tiempo (por defecto 300 segundos)
        self.window = timedelta(seconds=window_seconds)
        # Permite inyectar una función personalizada para obtener la hora actual (útil para tests)
        self.now_fn = now_fn or datetime.utcnow
        # Inicializa la estructura de datos como una deque vacía
        self._data = deque()

    def add(self, log_entry):
        # Obtiene el timestamp del objeto Log
        ts = log_entry.timestamp
        # Obtiene la hora actual
        now = self.now_fn()
        # Si el timestamp es del futuro, no lo agrega
        if ts > now:
            return
        # Agrega el registro junto con su timestamp a la cola
        self._data.append((ts, log_entry))
        # Elimina los registros que estén fuera de la ventana de tiempo
        self._evict_old()

    def _evict_old(self):
        # Obtiene la hora actual
        now = self.now_fn()
        # Elimina los registros más antiguos mientras estén fuera de la ventana de tiempo
        while self._data and now - self._data[0][0] > self.window:
            self._data.popleft()

    def get_all(self):
        # Limpia los registros viejos antes de devolver los actuales
        self._evict_old()
        # Devuelve solo los objetos Log almacenados actualmente
        return [entry for (_, entry) in self._data]