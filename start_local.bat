@echo off
title Syris 2.0 Launcher
echo ========================================================
echo   Starting Syris 2.0 AI JEE Study Companion (Local)
echo ========================================================
echo.
echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "Syris Backend (FastAPI :8000)" cmd /k "cd /d ""%~dp0"" && backend\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --port 8000"

timeout /t 2 /nobreak >nul

echo [2/2] Starting Next.js Frontend on http://localhost:3000 ...
start "Syris Frontend (Next.js :3000)" cmd /k "cd /d ""%~dp0frontend"" && npm run dev"

echo.
echo ========================================================
echo   Servers are now running in separate terminal windows:
echo   - Frontend: http://localhost:3000
echo   - Backend Docs: http://127.0.0.1:8000/api/v1/docs
echo ========================================================
echo.
pause
