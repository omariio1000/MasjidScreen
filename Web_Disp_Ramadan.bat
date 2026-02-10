@echo off
cd /d "%~dp0"
echo Checking for updates...
git fetch
git status
cd /d "%~dp0"\code
echo Starting Python script...
python web_display.py -r
pause
