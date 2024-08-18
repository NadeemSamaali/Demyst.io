@echo off

REM Setting directory to current current file path
cd /d %~dp0

REM Activating virtual environment
call env/Scripts/activate

REM Run Flask server
start py -m main

REM Allow some time for the Flask server to start
timeout /t 10 >nul

REM Open the Flask application in the default web browser
start static/index.html
