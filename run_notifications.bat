@echo off
cd /d "c:\Users\Dell\Desktop\Hackathon\Aamcare vaccine updated"
call venv\Scripts\activate
python manage.py send_daily_notifications
pause
