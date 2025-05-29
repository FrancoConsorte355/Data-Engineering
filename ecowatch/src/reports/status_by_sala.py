# src/reports/status_by_sala.py
from .report_interface import Report
from collections import defaultdict
from src.reports.strategies.metric import AvgStrategy, MaxStrategy, MinStrategy

class ReportStatusBySala(Report):
    """
    Generates for each sala the list of logs in the window
    and computes metrics via injected MetricStrategy instances.
    """
    def __init__(self, strategies=None):
        # Default strategies for temperatura, humedad, co2
        self.strategies = strategies or [
            AvgStrategy('temperatura'), MaxStrategy('temperatura'), MinStrategy('temperatura'),
            AvgStrategy('humedad'),    MaxStrategy('humedad'),    MinStrategy('humedad'),
            AvgStrategy('co2'),        MaxStrategy('co2'),        MinStrategy('co2')
        ]

    def generate(self, records):
        grouped = defaultdict(list)
        for r in records:
            grouped[r.sala].append(r)

        result = {}
        for sala, logs in grouped.items():
            # Prepare metrics dict grouped by field
            metrics = {}
            for strat in self.strategies:
                field = strat.field_name
                if field not in metrics:
                    metrics[field] = {}
                metrics[field][strat.metric_name] = strat.compute(logs)

            result[sala] = {
                'logs': logs,
                'metrics': metrics
            }
        return result