from app import app
import json
from flask import render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from os import listdir
from os.path import isfile, join
#import main

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
    matchDocs = [('Dokumen1', '100', '80', 'tes123')]
    if(queries == ""): matchDocs = []
 #   else: matchDocs = main.mainSearch(queries, externalUrls)
    return jsonify(matchDocs)

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
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    filenames= [f for f in listdir(app.config['UPLOAD_PATH']) if isfile(join(app.config['UPLOAD_PATH'], f))]  
    return jsonify(filenames)

@app.route('/deletefile', methods=['POST', 'GET'])
def deletefile():
    fileName = request.args['text']
    #fileName = request.form
    os.remove(join(app.config['UPLOAD_PATH'], fileName))
    filenames= [f for f in listdir(app.config['UPLOAD_PATH']) if isfile(join(app.config['UPLOAD_PATH'], f))]
    return jsonify(filenames)

if(__name__ == "__main__"):
    app.run(debug=True) 
    