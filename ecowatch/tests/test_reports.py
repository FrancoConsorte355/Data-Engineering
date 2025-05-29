# tests/test_reports.py
import unittest
from datetime import datetime, timedelta
from src.domain.log import Log
from src.reports.status_by_sala import ReportStatusBySala
from src.reports.critical_alerts import ReportCriticalAlerts

class TestReports(unittest.TestCase):
    def setUp(self):
        base = datetime.fromisoformat('2025-05-01T08:05:00')
        self.log1 = Log(timestamp=base - timedelta(minutes=1), sala='Room1', estado='INFO', temperatura=22.0, humedad=55.0, co2=700.0, mensaje='m1')
        self.log2 = Log(timestamp=base - timedelta(minutes=2), sala='Room1', estado='ERROR', temperatura=20.0, humedad=50.0, co2=650.0, mensaje='m2')
        self.log3 = Log(timestamp=base - timedelta(minutes=3), sala='Room2', estado='INFO', temperatura=25.0, humedad=60.0, co2=800.0, mensaje='m3')
        self.logs = [self.log1, self.log2, self.log3]

    def test_status_by_sala(self):
        report = ReportStatusBySala()
        result = report.generate(self.logs)
        # Validar salas presentes
        self.assertIn('Room1', result)
        self.assertIn('Room2', result)
        # Cantidad de logs por sala
        self.assertEqual(len(result['Room1']['logs']), 2)
        self.assertEqual(len(result['Room2']['logs']), 1)
        # Métricas de temperatura
        temps = [22.0, 20.0]
        metrics1 = result['Room1']['metrics']
        self.assertAlmostEqual(metrics1['temperatura']['avg'], sum(temps)/len(temps))
        self.assertEqual(metrics1['temperatura']['max'], max(temps))
        self.assertEqual(metrics1['temperatura']['min'], min(temps))

    def test_critical_alerts(self):
        report = ReportCriticalAlerts()
        errors = report.generate(self.logs)
        # Sólo un log con estado ERROR
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].estado, 'ERROR')
        self.assertEqual(errors[0].sala, 'Room1')

if __name__ == '__main__':
    unittest.main()