@echo off
cd /d "%~dp0"
powershell -WindowStyle Hidden -Command "Start-Process python -ArgumentList 'web_api_qwen.py' -WindowStyle Hidden"
python gui_chat.py
