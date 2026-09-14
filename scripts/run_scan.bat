@echo off
setlocal
cd /d "%~dp0.."
if not exist .venv\Scripts\python.exe (
  echo Missing .venv. Create it with: py -m venv .venv
  exit /b 1
)
.venv\Scripts\python.exe scanner.py %*
endlocal
