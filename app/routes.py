from app import app
import json
from flask import render_template, request, jsonify


#Global variabel
externalUrls=""
internalDocs="2"

@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/search', methods=["POST", "GET"])
def search():
    #anggap tupel berbentuk (judul, jumlahkata, tingkat kemiripan, kalimat pertama)
    #default options adalah externaldoc kosong dan internal document 15
    queries = request.form.get("text")
    print(internalDocs)
    matchDocs = [("Dokumen 1", "100", "80", "tes 123"), ("Dokumen 2", "100", "80", "tes 123")]
    matchDocs = matchDocs[:int(internalDocs)]
    if(queries == ""): matchDocs = []
    # else: proses queries
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

if(__name__ == "__main__"):
    app.run(debug=True) 
    