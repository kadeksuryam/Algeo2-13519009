from app import app
import json
from flask import render_template, request, jsonify


@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/search', methods=["POST", "GET"])
def search():
    #anggap tupel berbentuk (judul, jumlahkata, tingkat kemiripan, kalimat pertama)
 #   searchbox = request.form.get("text", "inputsearch")
    query = request.form.get("text")
    messange = request.form.get("text")
    matchDocs = [("Dokumen 1", "100", "80", "tes 123"), ("Dokumen 2", "100", "80", "tes 123")]
    if(query == "1"): matchDocs = [matchDocs[0]]
    if(query == ""): matchDocs = []
    print(query)
    print(messange)
    return jsonify(matchDocs)

if(__name__ == "__main__"):
    app.run(debug=True) 
    