@echo off
cd /d "%~dp0"
set "PY=python"
where python >nul 2>nul || set "PY=%USERPROFILE%\anaconda3\python.exe"
"%PY%" -c "import flask" 2>nul || "%PY%" -m pip install flask
start "" http://127.0.0.1:5000/mahasiswa
"%PY%" app.py
pause
