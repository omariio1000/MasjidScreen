@echo on
cd /d "%~dp0"
git pull
cd /d "%~dp0"\code
cmd /k python emails.py
