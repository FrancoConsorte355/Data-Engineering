# src/reports/critical_alerts.py
from .report_interface import Report

class ReportCriticalAlerts(Report):
    """
    Filters and returns Log entries with estado == 'ERROR'.
    """
    def generate(self, records):
        return [r for r in records if r.estado == 'ERROR']