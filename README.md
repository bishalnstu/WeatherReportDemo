# Weather Report Demo

A small, offline Python project for showing **unit, component, and system
testing on the same feature**. It uses only the Python standard library.

## Setup on your Windows computer

1. Install Python 3 if necessary. Open PowerShell and check:
   `python --version`
2. Extract the whole `WeatherReportDemo` folder into:
   `C:\Users\*\`
3. Open PowerShell in the extracted `WeatherReportDemo` folder. No `pip
   install`, internet connection, SQLite server, or API key is needed.

To run the entire demonstration, double-click `run_demo.bat` or run
`cmd /c run_demo.bat` from PowerShell. The batch file runs all three test
groups and then the real application.

## The same feature at three levels

| Level | Real code under test | What is replaced? | Example |
| --- | --- | --- | --- |
| Unit | `summarize()` | Nothing; pass readings directly | [10, 12, 14] gives average 12 |
| Component | `WeatherReportService`, summarizer, formatter | The SQLite repository is replaced by a small fake | ST-01 report has three readings and average 12 |
| System | CLI, service, calculations, and real SQLite repository | Nothing; tests use a temporary database | Seed ST-01, run the command, check the full output |

The application has a public input boundary (CLI), a service, pure calculation
functions, and persistence. This makes the difference among the three levels
visible without needing a web server.

## Live classroom commands

Run these in the project folder:

```powershell
python app.py seed
python app.py report ST-01
python app.py report UNKNOWN
```

The first report displays three readings with average **12.0 C**. The unknown
station shows a clear error and exits with a nonzero status. `seed` is
idempotent: running it again does not duplicate the sample readings.

Show each testing level separately:

```powershell
python -m unittest tests.test_unit -v
python -m unittest tests.test_component -v
python -m unittest tests.test_system -v
```

Or run every test:

```powershell
python -m unittest discover -s tests -v
```

For a fresh manual database, remove `weather_demo.sqlite` from the project
folder or pass `--db` with a new filename. The automated system tests use
their own temporary databases and do not touch the manual demo database.


## Files

- `weather_core.py`: pure calculation, data structures, formatting
- `repository.py`: real SQLite storage
- `service.py`: report component and repository interface
- `app.py`: command-line entry point
- `tests/test_unit.py`, `test_component.py`, `test_system.py`: three levels
- `run_demo.bat`: Windows one-command demonstration
