@echo off
cd /d "%~dp0"
echo Checking for updates...
git status
cd /d "%~dp0"\code
echo Starting Python script...
cmd /k python masjid_display.py
