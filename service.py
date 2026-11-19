"""The component under test: repository + calculation + formatting."""

from typing import Protocol

from weather_core import Reading, format_report, summarize


class ReadingRepository(Protocol):
    def get_readings(self, station_id: str) -> list[Reading]:
        """Return readings for one station."""


class WeatherReportService:
    def __init__(self, repository: ReadingRepository) -> None:
        self.repository = repository

    def report_for(self, station_id: str) -> str:
        if not station_id.strip():
            raise ValueError("A station ID is required.")
        readings = self.repository.get_readings(station_id)
        return format_report(station_id, summarize(readings))
