@echo off
setlocal
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "AION_REPO=%~dp0.."
python "%AION_REPO%\src\aion_cli_entry.py" %*
if errorlevel 1 exit /b %errorlevel%
exit /b 0