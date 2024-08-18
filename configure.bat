REM @echo off

REM Setting the relative path to the path of the batch file
cd /d %~dp0

REM Creating virtual environment
py -m venv env

REM Activating virtual environment
call env\Scripts\activate

REM Installing necessary libraries
py -m pip install -r requirements.txt

pause