"""SQLite storage for weather readings."""

import sqlite3
from pathlib import Path

from weather_core import Reading


class SQLiteWeatherRepository:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY,
                    station_id TEXT NOT NULL,
                    observed_at TEXT NOT NULL,
                    temperature_c REAL NOT NULL,
                    UNIQUE(station_id, observed_at)
                )
                """
            )

    def add_reading(
        self, station_id: str, observed_at: str, temperature_c: float
    ) -> bool:
        """Insert a reading; return False if the timestamp already exists."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO readings
                    (station_id, observed_at, temperature_c)
                VALUES (?, ?, ?)
                """,
                (station_id, observed_at, temperature_c),
            )
            return cursor.rowcount == 1

    def get_readings(self, station_id: str) -> list[Reading]:
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT observed_at, temperature_c
                FROM readings
                WHERE station_id = ?
                ORDER BY observed_at
                """,
                (station_id,),
            ).fetchall()
        return [Reading(observed_at, temperature_c) for observed_at, temperature_c in rows]
