"""UNIT: exercise pure functions without a repository or CLI."""

import unittest

from weather_core import NoReadingsError, Reading, Summary, format_report, summarize


class SummaryUnitTests(unittest.TestCase):
    def test_three_readings(self):
        readings = [
            Reading("08:00", 10.0),
            Reading("09:00", 12.0),
            Reading("10:00", 14.0),
        ]
        self.assertEqual(summarize(readings), Summary(3, 12.0, 10.0, 14.0))

    def test_one_reading_is_its_own_minimum_maximum_and_average(self):
        self.assertEqual(summarize([Reading("08:00", -2.0)]), Summary(1, -2.0, -2.0, -2.0))

    def test_empty_readings_have_no_summary(self):
        with self.assertRaises(NoReadingsError):
            summarize([])

    def test_report_format_is_stable(self):
        text = format_report("ST-01", Summary(3, 12.0, 10.0, 14.0))
        self.assertIn("Station: ST-01", text)
        self.assertIn("Average: 12.0 C", text)


if __name__ == "__main__":
    unittest.main()
