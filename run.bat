@echo off
cd %CD%/
echo Creating the Virtual Environment...
py -3 -m venv venv

echo --------------------------------
echo Activating the Virtual Environment...
call venv\Scripts\activate

echo --------------------------------
echo Installing the Requirements...
pip install -r requirements.txt
py -m nltk.downloader punkt
py -m nltk.downloader stopwords
set FLASK_APP=searchengine.py

echo --------------------------------
echo Starting the Server...
flask run
PAUSE