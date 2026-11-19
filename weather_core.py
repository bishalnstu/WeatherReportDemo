"""Pure weather calculations and report formatting.

This module is the unit-testing target: it has no database or command-line
dependencies.
"""

from dataclasses import dataclass
from statistics import mean
from typing import Sequence


class NoReadingsError(LookupError):
    """The requested station has no temperature readings."""


@dataclass(frozen=True)
class Reading:
    observed_at: str
    temperature_c: float


@dataclass(frozen=True)
class Summary:
    count: int
    average_c: float
    minimum_c: float
    maximum_c: float


def summarize(readings: Sequence[Reading]) -> Summary:
    """Calculate a summary. A station with no readings cannot have a report."""
    if not readings:
        raise NoReadingsError("No readings are available for this station.")

    values = [reading.temperature_c for reading in readings]
    return Summary(
        count=len(values),
        average_c=mean(values),
        minimum_c=min(values),
        maximum_c=max(values),
    )

def format_report(station_id: str, summary: Summary) -> str:
    """Create the text displayed by the command-line application."""
    return (
        f"Station: {station_id}\n"
        f"Readings: {summary.count}\n"
        f"Average: {summary.average_c:.1f} C\n"
        f"Minimum: {summary.minimum_c:.1f} C\n"
        f"Maximum: {summary.maximum_c:.1f} C"
    )
