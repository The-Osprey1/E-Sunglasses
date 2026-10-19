@echo off
echo Plug in the QT Py and double-tap its reset button now.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install-to-board.ps1"
pause
