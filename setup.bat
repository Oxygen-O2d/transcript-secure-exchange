@echo off
echo Creating Python virtual environment...
python -m venv venv
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo Setup complete. You must activate the environment using `venv\Scripts\activate` before running the project.
