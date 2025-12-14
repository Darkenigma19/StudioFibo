@echo off
echo ========================================
echo Starting StudioFlow - Complete Stack
echo ========================================
echo.
echo This will open TWO windows:
echo   1. Backend Server (port 8000)
echo   2. Frontend Server (port 3000)
echo.
echo KEEP BOTH WINDOWS OPEN while using the app!
echo.
pause

echo Starting Backend Server...
start "StudioFlow Backend" cmd /k "cd /d E:\StudioFlow && call start_backend.bat"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "StudioFlow Frontend" cmd /k "cd /d E:\StudioFlow && call start_frontend.bat"

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Both servers starting...
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo Opening browser in 5 seconds...
echo ========================================

timeout /t 5 /nobreak >nul

start http://localhost:3000

echo.
echo Done! StudioFlow is running.
echo DO NOT CLOSE the Backend and Frontend terminal windows!
echo.
pause
