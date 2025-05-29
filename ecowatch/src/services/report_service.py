# src/services/report_service.py
from src.reports.factory import ReportFactory

class ReportService:
    def __init__(self, cache):
        self.cache = cache

    def generate(self, report_type: str):
        report = ReportFactory.get(report_type)
        return report.generate(self.cache.get_all())