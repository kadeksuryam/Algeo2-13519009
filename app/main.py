import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import re, os
import string
from collections import OrderedDict
from os import listdir
from os.path import isfile, join
import nltk
from nltk.tokenize import word_tokenize 
from nltk.tokenize import sent_tokenize
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

#$nltk.download()
'''
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
'''
def txtToStrings(txt_path):
    WORDS = []
    with open(txt_path, "r", encoding="mbcs") as file:
        for line in file.readlines():
            WORDS.append(line.rstrip())
    WORDS = ''.join(WORDS)   
    return WORDS

#searchquery sudah dalam vektor, tapi belum tunggal
def queryTunggal(query_words, query_words_tunggal):
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
'''
#Mengembalian array of tuple hasil
def processExternal(searchQuery_vector):
    urls = externalDoc.split()
    for url in urls:
        html = urllib.request.urlopen(url).read()
        html = htmlToStrings(html)
        html_vector = documentToVector(html, searchQuery)
        jml_kata = jumlahKata(html_vector)       
        kemiripan = similiarity(html_vector, searchQuery_vector)
        kalimat_pertama = firstSentence(html)

        search_result.append((url, jml_kata, kemiripan, kalimat_pertama))
    return "tes"
'''
def similiarity(searchQuery_vector, txt_file_vec):
    return "tes"

def getFirstSentence(txt_file_words):
    return "tes"

def processTXT(filePath, searchQuery_vector, query_words_tunggal): 
    #Ubah isi dalam TXT ke vektor, sebelumnya distemming dan dibersihkan dulu
    #Ubah txt ke string dulu
    txt_file_words = open(filePath).read()
    
    #bersihkan string
    cleanedString = cleanTheString(txt_file_words)
#    txt_file_words = [i[0] for i in cleanedString]
#    txt_file_words_vec = [i[1] for i in cleanedString]

    #daptkan vektor sesuai query_words_tunggal
    txt_file_vec = []
    txt_file_terms = []
    for word_query in query_words_tunggal:
        cntWord = 0
        isFound = False
        for i in range(0, len(cleanedString)):
            if(word_query == cleanedString[i][0]):
                cntWord = cleanedString[i][1]
                txt_file_terms.append(cleanedString[i])
                isFound = True
                break
        if(not(isFound)): txt_file_terms.append((word_query, 0))
        else: txt_file_vec.append(cntWord)
    
    #sampai disini vector yang sesuai query sudah selesai dibuat

    #nama dokumen tidak diproses disini

    #cari similiarity
    kemiripan = similiarity(searchQuery_vector, txt_file_vec)
    
    #cari jumlah kata
    jumlahkata = len(txt_file_words.split())

    #dapatkan kalimat pertama dengan ntlk
    kalimatPertama = getFirstSentence(txt_file_words)

    
    return kemiripan, jumlahkata, kalimatPertama, txt_file_terms
'''
def processHTML(filePath=None, searchQuery_vector, query_words_tunggal): 
    return "tes"
'''
def processHTML(searchQuery_vector, query_words_tunggal, filePath=None, URLs=None):
    return "tes" 

#Mengembalikan array of tuple hasil    
def processInternal(searchQuery_vector, query_words_tunggal):
    basedir = os.path.abspath(os.path.dirname(__file__))

    hasil_internal = []
    #proses semua txt
    internal_txt_path = os.path.join(basedir, 'static/uploads/txt/')
    for f in listdir(internal_txt_path):
        if(isfile(join(internal_txt_path, f))):
            kemiripan, jumlahkata, kalimatPertama, terms = processTXT(join(internal_txt_path, f), searchQuery_vector, query_words_tunggal)
            hasil_internal.append((f[:len(f)-4], kemiripan, jumlahkata, kalimatPertama, terms))
        #    print(terms)
        #print(f)
    '''
    #proses semua html
    external_html_path = os.path.join(basedir, 'static/uploads/html/')
    for f in listdir(external_html_path):
        if(isfile(f)): processHTML(join(internal_txt_path, f), searchQuery_vector, query_words_tunggal)
        #print(f)
    '''
    return hasil_internal

def cleanTheString(strings):
    #bersihkan dokumen terlebih dahulu dengan regex

    #hapus unicode
    strings = re.sub(r'[^\x00-\x7F]+', ' ', strings)
    #hapus mentions
    strings = re.sub(r'@\w+', '', strings)
    #lowercase the string
    strings = strings.lower()
    #hapus punctuation (titik, koma, dsb)'
    strings = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', strings)
    #hapus angka
    strings = re.sub(r"\d+", "", strings)
    #hapus whitespace
    strings = strings.strip()

    #lakukan filtering dengan sastrawi
    factory_stop_word = StopWordRemoverFactory()
    stopword = factory_stop_word.create_stop_word_remover()
    strings = stopword.remove(strings)

    #lakukan stemming dengan sastrawi
    factory_stemmer = StemmerFactory()
    stemmer = factory_stemmer.create_stemmer()
    strings = stemmer.stem(strings)

    #hitung kemunculan setiap terms dalam pair (kata, jumlah_kemunculan)
    strings = strings.split()
    strings_tunggal = list(OrderedDict.fromkeys(strings))
    hasil = []
    for word_tunggal in strings_tunggal:
        cntWord = 0
        for word in strings:
            if(word == word_tunggal): cntWord += 1
        hasil.append((word_tunggal, cntWord))
    
    return hasil
    
def mainSearch(searchQuery, externalDoc=""):
    #ubah queries menjadi vektor terlebih dahulu
    
    #bersihkan query, lakukan stemming, filtering (hapus stopwords)
    cleaned_query = cleanTheString(searchQuery)
    vector_query = [i[1] for i in cleaned_query]
    query_words = [i[0] for i in cleaned_query]

    search_result = []
#    print(vector_query)
#    print(query_words)
    #proses internal dokumen
    search_result += processInternal(vector_query, query_words)

    #proses external dokumen
#    search_result += processExternal(vector_query, query_words, externalURLs)

    return search_result


if(__name__ == "__main__"):  
    print(mainSearch("jepang indonesia jepang"))
    #print(htmlToStrings(html))
    #print(htmlToStrings("https://en.wikipedia.org/wiki/Computer_science"))