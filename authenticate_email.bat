@echo on
cd /d "%~dp0"
git pull
cmd /k python emails.py
