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
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords
from math import sqrt

nltk.download('stopwords')
nltk.download('punkt')
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
def similiarity(searchQuery_vector, doc_vec, doc):
    sum = 0
    idx = 0
    square_doc = 0
    square_search = 0
    for kata in doc_vec:
        sum += searchQuery_vector[idx] * doc_vec[idx]
        square_search += (searchQuery_vector[idx]) ** 2
        idx += 1
    for kata in doc:
        square_doc += kata[1]
    if((square_search != 0) and (square_doc != 0)):
        return(100*sum/(sqrt(square_doc * square_search)))
    else:
        return 0

def getFirstSentence(txt_file_words):
    return nltk.sent_tokenize(txt_file_words)[0]

def processTXT(filePath, searchQuery_vector, query_words_tunggal): 
    #Ubah isi dalam TXT ke vektor, sebelumnya distemming dan dibersihkan dulu
    #Ubah txt ke string dulu
    txt_file_words = open(filePath, encoding="utf8").read()
    
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
        txt_file_vec.append(cntWord)
    
    #sampai disini vector yang sesuai query sudah selesai dibuat

    #nama dokumen tidak diproses disini

    #cari similiarity
    kemiripan = similiarity(searchQuery_vector, txt_file_vec, cleanedString)
    
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
        #    terms = [list(item) for item in terms]
            if(len(terms) != 0): 
                hasil_internal.append((f[:len(f)-4], jumlahkata, kemiripan, kalimatPertama, 'internal', terms))
 
    '''
    #proses semua html
    external_html_path = os.path.join(basedir, 'static/uploads/html/')
    for f in listdir(external_html_path):
        if(isfile(f)): processHTML(join(internal_txt_path, f), searchQuery_vector, query_words_tunggal)
        #print(f)
    '''
 #   print(hasil_internal)
    x = lambda s : s[2]
    hasil_internal.sort(reverse = True, key = x)
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

    #lakukan filtering dengan nltk
    tokens = word_tokenize(strings)
    listStopword =  set(stopwords.words('english'))

    removed = []
    for t in tokens:
        if t not in listStopword:
            removed.append(t)
    strings = " ".join(removed)

    #lakukan stemming dengan nltk
    ps = PorterStemmer()
    stemmed_string = []
    for word in strings.split():
        stemmed_string.append(ps.stem(word))
    strings = ' '.join(stemmed_string)

#    print(stemmed_string)
    #hitung kemunculan setiap terms dalam pair (kata, jumlah_kemunculan)
    strings = strings.split()
    strings_tunggal = list(OrderedDict.fromkeys(strings))
    hasil = []
    for word_tunggal in strings_tunggal:
        cntWord = 0
        for word in strings:
            if(word == word_tunggal): cntWord += 1
        hasil.append((word_tunggal, cntWord))
#    print(hasil)
    return hasil
    
def mainSearch(searchQuery, externalDoc=""):
    #ubah queries menjadi vektor terlebih dahulu
    
    #bersihkan query, lakukan stemming, filtering (hapus stopwords)
    cleaned_query = cleanTheString(searchQuery)
    
    vector_query = [i[1] for i in cleaned_query]
    query_words = [i[0] for i in cleaned_query]
    
#    print(query_words)
    search_result = []
#    print(vector_query)
#    print(query_words)
    #proses internal dokumen
    search_result += processInternal(vector_query, query_words)
    
    #proses external dokumen

    #setelah internal dan external sudah diproses, pecah data menjadi dua bagian
    vec_terms_res = [i[5] for i in search_result]

    for i in range(0, len(vec_terms_res)):
        for j in range(0, len(vec_terms_res[i])):
            vec_terms_res[i][j] = vec_terms_res[i][j][1]
    vec_terms = [vector_query] + vec_terms_res
    
#    print(vec_terms)
    return search_result, query_words, vec_terms
    
#    return "test"


if(__name__ == "__main__"):  
    mainSearch("tes satu dua")
    #print(htmlToStrings(html))
    #print(htmlToStrings("https://en.wikipedia.org/wiki/Computer_science"))