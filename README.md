# A Search Engine by Puroguramaa Okarishimasu

# [insert]
[insert] is a search engine based on similiarity between content queries and documents that's computed by vectorizing the search query and documents then the similiarity can be computed using cosine formula a.k.a similiarity formula between two vectors.

## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Requirements](#requirements)
* [Setting Up](#setting-up)
* [Running](#running)
* [Project Structure](#project-structure)
* [How to Use](#how-to-use)
* [Authors](#authors)


## General info
This project is a project that is obligatory in ITB Linear Algebra and Geometric Course class 2020. We're expected to build a search engine website that's can find out similiarity between each documents (txt and html) that's given by user and the search queries using linear algebra concepts like vector and dot product. This project is build using two different framework that is Bootstrap for front-end and Flask for backend, also, javascript especially jQuery as connector between front-end and back-end and ofcourse html for website basic structure. 

## Screenshots
![main](./img/screenshot.png)

## Requirements
- Make sure you have already installing python3, you can check them inside `cmd` by typing `py --version`
- All requirements is inside `requirements.txt` file, you can install each requirement using python package manager (pip), by typing  `pip install package`, where package is the name package/library that's you want to install or you can just run the `run.bat` file and let the batch file do the work.

  
## Setting Up
- Clone this github repository, and create a python virtual environment using this command : `py -3 -m venv [ve]` where [ve] is the virtual environment's name you can named that with anything
- After virtual environment has created you can activate that using `[ve]\Scripts\activate`, where [ve] is your virtual environment's name.
- Install all requirements above
- Alternatively, you can just run the batch file that's do all the work (setting up and running the server)

## Running

- To run the server, firstly you need setting the flask environment variable to `searchengine.py` you can setting that by `set FLASK_APP=searchengine.py`
- After that, you can start the server by typing `flask run`
- Server has already started! You can view the website according the url which server assigned into, normally server will point to `http://127.0.0.1:5000/`
- Alternatively, you can just run the batch file that's do all the work (setting up and running the server)

## Project Structure

```
src
├───app
│   ├───static
|   |   |───css
|   |   |   └───main.css
|   |   ├───js
|   |   |   └───main.js
|   |   └───uploads
|   |       ├───html
|   |       └───txt
│   ├───templates
|   |   └───index.html
│   ├───__init__.py
│   ├───main.py
|   └───routes.py
|
├───venv
├───config.py
└───searchengine.py

```

## How to Use
- You can start searching the documents by typing some queries inside input query box
- The results will be displayed in "All results" tab
- You can configure the documents that's used in this search engine in "Options" tab
- Inside "Options" tab you can add external documents (urls) or upload your own documents (html and txt file)
- If you want to see the occurences of each term that's you input in search box, you can go to "Details" tab


## Authors
"Puroguramaa Okarishimasu", the creators of this search Engine is ITB student's whose are:
- Kadek Surya Mahardika (13519165)
- Akeyla Pradia Naufal (13519178)
- Mochammad Facturohman (13519009)




