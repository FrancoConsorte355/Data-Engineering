# src/services/ingest_service.py
from src.ingestion.readers.csv_reader import CsvReader
from src.ingestion.validators import Validator
from src.cache.temporal_cache import TemporalCache

class IngestService:
    """
    Coordinates reading raw logs, validating them, and adding domain Log objects to cache.
    """
    def __init__(self, reader=None, cache=None):
        self.reader = reader or CsvReader()
        self.cache = cache or TemporalCache()

    def run(self):
        for raw in self.reader.read_logs():
            try:
                log_obj = Validator.validate(raw)
                self.cache.add(log_obj)
            except ValueError:
                continue