@echo off
echo Activating the Virtual Environment...
venv\Scripts\activate
echo Installing the Requirements...
pip install -r requirements.txt
export FLASK_APP=searchengine.py
echo Starting the Server..
flask run
