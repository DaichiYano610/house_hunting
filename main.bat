@echo off
cd /d %~dp0
uvicorn main:app --port 8000 --reload
pause