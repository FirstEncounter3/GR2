echo off 
cls
echo Creating a virtual environment...
python -m venv venv 
echo ..done
echo installing dependencies...
venv\Scripts\pip install -r requirements.txt  
echo ..done
echo To run use run.bat or run_no_console.bat
pause