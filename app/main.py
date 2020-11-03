import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import re, os
import string

#sudah dalam strings
def cleanTheDocument(document):
    # Remove Unicode
    document_test = re.sub(r'[^\x00-\x7F]+', ' ', document)
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


def htmlToStrings(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in texts:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return cleanTheDocument(output)
#    visible_texts = filter(tag_visible, texts)  
#    return u" ".join(t.strip() for t in visible_texts)

def txtToStrings(txt_path):
    WORDS = []
    with open(txt_path, "r", encoding="mbcs") as file:
        for line in file.readlines():
            WORDS.append(line.rstrip())
    WORDS = ''.join(WORDS)
    WORDS = cleanTheDocument(WORDS)    
    return WORDS

#searchquery sudah dalam string
def queryToVector(searchQuery):
    query_words = searchQuery.split()
    query_words_tunggal = list(set(query_words))
    query_kemunculan = []
    for word_set in query_words_tunggal:
        cntKemunculan = 0
        for word_list in query_words:
            if(word_set == word_list):
                cntKemunculan += 1
        query_kemunculan.append(cntKemunculan)
    return query_kemunculan

#document sudah dalam string
#search query sudah dalam vector of words
def documentToVector(document, searchQuery):
    doc_words = document.split()
    query_kemunculan = []
    for query in searchQuery:
        cntKemunculan = 0
        for word in doc_words:
            if(word == query): cntKemunculan += 1
        query_kemunculan.append(cntKemunculan)
    return query_kemunculan

def mainSearch(searchQuery, externalDoc=None, internalDoc=None):
    #internalDoc --> jumlah document internal
    #externalDoc --> list of urls
    #searchQuery --> dalam string, ubah ke vektor terlebih dahulu
    search_result = []
    searchQuery_vector = queryToVector(searchQuery)

    #process external doc
    urls = externalDoc.split()
    for url in urls:
        html = urllib.request.urlopen(url).read()
        html = htmlToStrings(html)
        html_vector = documentToVector(hmtl, searchQuery)
        jml_kata = jumlahKata(html, searchQuery)       
        kemiripan = similiarity(html_vector, searchQuery_vector)
        kalimat_pertama = firstSentence(html)

        search_result.append((url, jml_kata, kemiripan, kalimat_pertama))

    #process internal doc
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_file = os.path.join(basedir, 'static/txt/doc1.txt')
    print("tes")

if(__name__ == "__main__"):  
    
    print(htmlToStrings(html))
    #print(htmlToStrings("https://en.wikipedia.org/wiki/Computer_science"))