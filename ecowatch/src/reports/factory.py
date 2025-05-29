# src/reports/factory.py
from .status_by_sala import ReportStatusBySala
from .critical_alerts import ReportCriticalAlerts
from .report_interface import Report
from .pandas_status_report import PandasStatusReport

class ReportFactory:
    _reports = {
        'status_by_sala': ReportStatusBySala,
        'critical_alerts': ReportCriticalAlerts,
        'pandas_status': PandasStatusReport,
        'pandas_status_report': PandasStatusReport  # alias for pandas_status
    }
    
    @classmethod
    def get(cls, report_type: str) -> Report:
        if report_type not in cls._reports:
            raise ValueError(f"Unknown report type: {report_type}")
        return cls._reports[report_type]()