from app import app
import requests
from bs4 import BeautifulSoup
import flask

import re

#sudah dalam strings
def cleanTheDocument(document):
    # Remove Unicode
    document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
    # Remove Mentions
    document_test = re.sub(r'@\w+', '', document_test)
    # Lowercase the document
    document_test = document_test.lower()
    # Remove punctuations
    document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
    # Lowercase the numbers
    document_test = re.sub(r'[0-9]', '', document_test)
    # Remove the doubled space
    document_test = re.sub(r'\s{2,}', ' ', document_test)
    return document_test


#sudah dalam string
def htmlToStrings(url):
    #Make a request
    r = requests.get(url)
    #Create an object to parse the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    # Retrieve all paragraphs and combine it as one
    sen = []
    for i in soup.find('div', {'class':'read__content'}).find_all('p'):
        sen.append(i.text)

    return cleanTheDocument(''.join(sen))

def txtToStrings(txt_path):
    WORDS = []
    with open(data_file, "r") as file:
        for line in file.readlines():
            WORDS.append(line.rstrip())
    WORDS = ''.join(WORDS)    
    return WORDS


class Document:
    def __init__(self, txtDoc=None, htmlDoc=None):
        if(txtDoc != None): print("none")
        if(htmlDoc != None):
            basedir = os.path.abspath(os.path.dirname(__file__))
            for i in range(0, amount+1):    
                txt_path = os.path.join(basedir, 'static/documents/doc' + str(i) + '.txt')




def mainSearch(searchQuery):
    print("test")


@app.route('/')
@app.route('/index.html')
def index():
    return flask.render_template("index.html")

@app.route('/search/', methods=['POST'])
def search():
    #anggap tupel berbentuk (judul, jumlahkata, tingkat kemiripan, kalimat pertama)
    templateArg = """
        <ol>
            {% for doc in docs %}
                <li>
                    <p>{{doc[0]}}</p>
                </li>
                <p>Jumlah kata: {{doc[1]}} </p>
                <p>Tingkat Kemiripan: {{doc[2]}} %</p>
                <p>{{doc[3]}}</p>
                <br/>
            {% endfor %}
        </ol>
    """
    #panggil fungsi mainSearch yang mengembalikan list of tuple
    searchQuery = flask.request.form.get('search', None)
    matchDocs = [("Dokumen 1", "100", "80", "tes 123")]
    if(searchQuery == None): matchDocs = []
    return flask.render_template_string(templateArg, docs=matchDocs)
    