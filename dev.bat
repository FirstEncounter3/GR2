echo off 
cls
echo Creating a virtual environment...
python -m venv venv 
echo ..done
echo installing dependencies...
venv\Scripts\pip install -r requirements.txt
venv\Scripts\pip install pyinstaller
echo ..done
echo Build to binary file...
call venv\Scripts\activate
pyinstaller -i ico\ico.ico main.py
echo ...done
pause