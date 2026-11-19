"""Weather report command-line application.

Run 'python app.py --help' to see the available commands.
"""

import argparse
from pathlib import Path

from repository import SQLiteWeatherRepository
from service import WeatherReportService
from weather_core import NoReadingsError


SAMPLE_READINGS = (
    ("ST-01", "2026-11-09T08:00", 10.0),
    ("ST-01", "2026-11-09T09:00", 12.0),
    ("ST-01", "2026-11-09T10:00", 14.0),
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Small weather report demo")
    parser.add_argument(
        "--db", default="weather_demo.sqlite", type=Path,
        help="SQLite file (default: weather_demo.sqlite)",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("seed", help="Insert three sample readings for ST-01")
    report = commands.add_parser("report", help="Display a station report")
    report.add_argument("station_id")
    add = commands.add_parser("add", help="Store one reading")
    add.add_argument("station_id")
    add.add_argument("observed_at", help="For example 2026-11-09T11:00")
    add.add_argument("temperature_c", type=float)
    args = parser.parse_args()

    repository = SQLiteWeatherRepository(args.db)

    if args.command == "seed":
        count = sum(repository.add_reading(*reading) for reading in SAMPLE_READINGS)
        print(f"Added {count} sample readings for ST-01.")
        return 0

    if args.command == "add":
        inserted = repository.add_reading(
            args.station_id, args.observed_at, args.temperature_c
        )
        if not inserted:
            parser.exit(2, "Error: that station already has a reading at this time.\n")
        print(f"Saved a reading for {args.station_id}.")
        return 0

    try:
        print(WeatherReportService(repository).report_for(args.station_id))
    except (NoReadingsError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
