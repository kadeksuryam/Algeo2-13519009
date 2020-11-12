from app import app
import json
from flask import render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from os import listdir
from os.path import isfile, join
from .main import mainSearch

#Global variabel
externalUrls=""

@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/search', methods=["POST", "GET"])
@app.route('/')
def search():
    #anggap tupel berbentuk (judul, jumlahkata, tingkat kemiripan, kalimat pertama, [(term, nq, nd1, nd2...)])
    queries = request.form.get("text")
    if(queries == ""): matchDocs, terms, vec_terms = [], [], []
    else: matchDocs, terms, vec_terms = mainSearch(queries)
 #   else: matchDocs = main.mainSearch(queries, externalUrls)
    return jsonify({"result" : matchDocs, "terms" : terms, "vec_terms": vec_terms})

@app.route('/externalDoc', methods=["POST", "GET"])
def externalURLs():
    global externalUrls
    externalUrls = request.form.get("text")
    return "", 204

@app.route('/internalDoc', methods=["POST", "GET"])
def internalDocuments():
    global internalDocs
    internalDocs = request.form.get("text")
    print(internalDocs)
    if(internalDocs == ""): internalDocs = "0"
    return "", 204

@app.route('/uploadajax', methods=['POST', 'GET'])
def upload():
    if(request.method == 'POST'):
        for uploaded_file in request.files.getlist('files[]'):
            filename = secure_filename(uploaded_file.filename)
            file_ext = os.path.splitext(filename)[1]
            if(file_ext not in app.config['UPLOAD_EXTENSIONS']):
                return "", 404
            if(file_ext == '.txt'): uploaded_file.save(os.path.join(join(app.config['UPLOAD_PATH'], 'txt'), filename))
            else: uploaded_file.save(os.path.join(join(app.config['UPLOAD_PATH'], 'html'), filename))
    filenames=[f for f in listdir(join(app.config['UPLOAD_PATH'], 'txt')) if isfile(join(join(app.config['UPLOAD_PATH'], 'txt'), f))]  
    filenames+=[f for f in listdir(join(app.config['UPLOAD_PATH'], 'html')) if isfile(join(join(app.config['UPLOAD_PATH'], 'html'), f))]  
    return jsonify(filenames)

@app.route('/deletefile', methods=['POST', 'GET'])
def deletefile():
    fileName = request.args['text']
    #fileName = request.form
    file_ext = os.path.splitext(fileName)[1]
    print(file_ext)
    if(file_ext == '.txt'): os.remove(join(join(app.config['UPLOAD_PATH'], 'txt'), fileName))
    else: os.remove(join(join(app.config['UPLOAD_PATH'], 'html'), fileName))
    filenames=[f for f in listdir(join(app.config['UPLOAD_PATH'], 'txt')) if isfile(join(join(app.config['UPLOAD_PATH'], 'txt'), f))]  
    filenames+=[f for f in listdir(join(app.config['UPLOAD_PATH'], 'html')) if isfile(join(join(app.config['UPLOAD_PATH'], 'html'), f))] 
    return jsonify(filenames)

if(__name__ == "__main__"):
    app.run(debug=True) 
    