"""SYSTEM: run the real CLI, service, and SQLite repository together."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
APP = PROJECT / "app.py"


class WeatherSystemTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.db = Path(self.temp_directory.name) / "weather.sqlite"

    def run_app(self, *arguments):
        return subprocess.run(
            [sys.executable, str(APP), "--db", str(self.db), *arguments],
            cwd=PROJECT, text=True, capture_output=True, check=False,
        )

    def test_seed_and_report_end_to_end(self):
        self.assertEqual(self.run_app("seed").returncode, 0)
        result = self.run_app("report", "ST-01")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Station: ST-01", result.stdout)
        self.assertIn("Readings: 3", result.stdout)
        self.assertIn("Average: 12.0 C", result.stdout)
        self.assertIn("Minimum: 10.0 C", result.stdout)
        self.assertIn("Maximum: 14.0 C", result.stdout)

    def test_unknown_station_is_a_clear_failure(self):
        result = self.run_app("report", "UNKNOWN")
        self.assertEqual(result.returncode, 2)
        self.assertIn("No readings are available", result.stderr)

    def test_add_then_report_persists_between_processes(self):
        added = self.run_app("add", "ST-02", "2026-11-09T08:00", "-2.5")
        report = self.run_app("report", "ST-02")
        self.assertEqual(added.returncode, 0, added.stderr)
        self.assertEqual(report.returncode, 0, report.stderr)
        self.assertIn("Average: -2.5 C", report.stdout)

    def test_seeding_twice_does_not_duplicate_readings(self):
        first = self.run_app("seed")
        second = self.run_app("seed")
        report = self.run_app("report", "ST-01")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(second.returncode, 0)
        self.assertIn("Added 0 sample readings", second.stdout)
        self.assertIn("Readings: 3", report.stdout)


if __name__ == "__main__":
    unittest.main()
