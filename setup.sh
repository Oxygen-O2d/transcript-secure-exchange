#!/bin/bash
echo "Creating Python virtual environment..."
python3 -m venv venv
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Setup complete. You must activate the environment using 'source venv/bin/activate' before running the project."
