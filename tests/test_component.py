"""COMPONENT: test the report service with a fake repository.

The service, calculation, and formatter are real. Only database access is
replaced, so this test focuses on the component's public interface.
"""

import unittest

from service import WeatherReportService
from weather_core import NoReadingsError, Reading


class FakeReadingRepository:
    def __init__(self, data):
        self.data = data
        self.requested_ids = []

    def get_readings(self, station_id):
        self.requested_ids.append(station_id)
        return self.data.get(station_id, [])

class ReportComponentTests(unittest.TestCase):
    def test_service_fetches_summarizes_and_formats(self):
        repository = FakeReadingRepository({
            "ST-01": [Reading("08:00", 10.0), Reading("09:00", 12.0),
                      Reading("10:00", 14.0)],
        })
        report = WeatherReportService(repository).report_for("ST-01")

        self.assertEqual(repository.requested_ids, ["ST-01"])
        self.assertIn("Readings: 3", report)
        self.assertIn("Average: 12.0 C", report)
        self.assertIn("Minimum: 10.0 C", report)
        self.assertIn("Maximum: 14.0 C", report)

    def test_service_does_not_mix_up_stations(self):
        repository = FakeReadingRepository({
            "ST-01": [Reading("08:00", 10.0)],
            "ST-02": [Reading("08:00", 20.0)],
        })
        report = WeatherReportService(repository).report_for("ST-02")
        self.assertEqual(repository.requested_ids, ["ST-02"])
        self.assertIn("Average: 20.0 C", report)

    def test_service_propagates_missing_readings(self):
        repository = FakeReadingRepository({})
        with self.assertRaises(NoReadingsError):
            WeatherReportService(repository).report_for("UNKNOWN")
        self.assertEqual(repository.requested_ids, ["UNKNOWN"])

    def test_blank_station_id_does_not_reach_repository(self):
        repository = FakeReadingRepository({})
        with self.assertRaises(ValueError):
            WeatherReportService(repository).report_for(" ")
        self.assertEqual(repository.requested_ids, [])


if __name__ == "__main__":
    unittest.main()
