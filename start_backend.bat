@echo off
echo ========================================
echo Starting StudioFlow Backend Server
echo ========================================
echo.

cd /d E:\StudioFlow

echo Activating Python virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting backend on http://127.0.0.1:8000
echo Press Ctrl+C to stop
echo.

python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000

pause
