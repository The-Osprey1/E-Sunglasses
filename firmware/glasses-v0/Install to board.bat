@echo off
echo Copying the glasses program onto the QT Py. Keep it plugged in.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install-to-board.ps1"
pause
