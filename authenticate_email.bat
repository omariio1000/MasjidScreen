@echo on
cd /d "%~dp0"
git pull
cd /d "%~dp0"\code
python emails.py
pause
