@echo off
cd /d "%~dp0"
start cmd /k "python web_api_qwen.py"
python gui_chat.py
