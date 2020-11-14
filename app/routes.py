from app import app
import json
from flask import render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from os import listdir
from os.path import isfile, join
from .main import mainSearch
import urllib.request
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
    else: matchDocs, terms, vec_terms = mainSearch(queries, externalUrls)
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
    txt_path = join(app.config['UPLOAD_PATH'], 'txt')
    html_path = join(app.config['UPLOAD_PATH'], 'html')
    if(request.method == 'POST'):
        for uploaded_file in request.files.getlist('files[]'):
            filename = secure_filename(uploaded_file.filename)
            file_ext = os.path.splitext(filename)[1]
            if(file_ext not in app.config['UPLOAD_EXTENSIONS']):
                return "", 404
            if(file_ext == '.txt'): uploaded_file.save(os.path.join(txt_path, filename))
            else: uploaded_file.save(os.path.join(html_path, filename))
    #rename file
    [os.rename(os.path.join(txt_path, f), os.path.join(txt_path, f).replace(' ', '_').lower()) for f in os.listdir(txt_path)]
    [os.rename(os.path.join(html_path, f), os.path.join(html_path, f).replace(' ', '_').lower()) for f in os.listdir(html_path)]
    filenames=[f for f in listdir(txt_path) if isfile(join(txt_path, f))]  
    filenames+=[f for f in listdir(html_path) if isfile(join(html_path, f))]  
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

@app.route('/search/<path:path>')
def get_files(path):
    if(path[len(path)-3:] == 'txt'):
        file_path = join(join(app.config['UPLOAD_PATH'], 'txt'), path)
        with open(file_path) as f:
                file_content = f.read()
        return file_content
    else:
        #file_path = join(join(app.config['UPLOAD_PATH'], 'html'), path)
        #f = open(file_path)
        return send_from_directory(join(app.config['UPLOAD_PATH'], 'html'), path)
    

if(__name__ == "__main__"):
    app.run(debug=True) 
    