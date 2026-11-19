@echo off
setlocal
cd /d "%~dp0"

echo Checking Python...
python --version
if errorlevel 1 goto failure

echo.
echo === 1. UNIT TESTS: calculations only ===
python -m unittest tests.test_unit -v
if errorlevel 1 goto failure

echo.
echo === 2. COMPONENT TESTS: service with fake repository ===
python -m unittest tests.test_component -v
if errorlevel 1 goto failure

echo.
echo === 3. SYSTEM TESTS: CLI + real temporary SQLite databases ===
python -m unittest tests.test_system -v
if errorlevel 1 goto failure

echo.
echo === LIVE APPLICATION ===
set "DEMO_DB=%TEMP%\weather_report_class_%RANDOM%.sqlite"
python app.py --db "%DEMO_DB%" seed
if errorlevel 1 goto failure
python app.py --db "%DEMO_DB%" report ST-01
if errorlevel 1 goto failure
echo.
echo All demonstrations passed. Temporary live database: %DEMO_DB%
exit /b 0

:failure
echo.
echo A command failed. Review the error shown above.
exit /b 1
