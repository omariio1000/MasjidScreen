@echo off
cd /d "%~dp0"
git pull
echo Starting Python script...
cmd /k python masjid_display.py -r
