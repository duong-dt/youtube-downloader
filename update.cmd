@echo off
.\.venv\Scripts\python.exe -m pip install pytube --upgrade
.\.venv\Scripts\python.exe -m pip freeze > requirements.txt