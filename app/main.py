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
import requests

nltk.download('stopwords')
nltk.download('punkt')

def htmlToStrings(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    '''
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
        'style',
        'nav',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in texts:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return output
#    visible_texts = filter(tag_visible, texts)  
#    return u" ".join(t.strip() for t in visible_texts)
    '''
    return texts

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
        square_doc += (kata[1]) ** 2
    if((square_search != 0) and (square_doc != 0)):
        return(100*sum/(sqrt(square_doc * square_search)))
    else:
        return 0

def getFirstSentence(txt_file_words):
    return sent_tokenize(txt_file_words)[0]

def processTXT(txt_file_words, searchQuery_vector, query_words_tunggal): 
    #Ubah isi dalam TXT ke vektor, sebelumnya distemming dan dibersihkan dulu
    #Ubah txt ke string dulu
    
    #bersihkan string
    cleanedString, _ = cleanTheString(txt_file_words)
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
def processHTML(filePath, urls, searchQuery_vector, query_words_tunggal):
    soup = BeautifulSoup(html, "html.parser")
    text_html = soup.get_text()
    #bersihkan string
    cleanedString, _ = cleanTheString(txt_html)
    kemiripan = 
    jumlah kata = 
    return 
'''
def processExternal(externalDoc, searchQuery_vector, query_words_tunggal):
    #lakukan request
    urls = externalDoc.split()
    hasil_external = []
    for url in urls:
        html = requests.get(url)
        #setiap html yang diterima, lakukan processing
        soup = BeautifulSoup(html.content, 'html.parser')
        #texts = soup.findAll(text=True)
        texts = []
        for i in soup.find_all('p'):
            texts.append(i.text)

        kemiripan, jumlahkata, kalimatPertama, terms = processTXT(" ".join(texts), searchQuery_vector, query_words_tunggal)
        if(len(terms) != 0): 
            hasil_external.append((soup.title.string, jumlahkata, kemiripan, kalimatPertama, url, terms))
        
    return hasil_external
#Mengembalikan array of tuple hasil    
def processInternal(searchQuery_vector, query_words_tunggal):
    basedir = os.path.abspath(os.path.dirname(__file__))

    hasil_internal = []
    #proses semua txt
    internal_txt_path = os.path.join(basedir, 'static/uploads/txt/')
    for f in listdir(internal_txt_path):
        if(isfile(join(internal_txt_path, f))):
            txt_file_words = open(join(internal_txt_path, f), encoding="utf8").read()
            kemiripan, jumlahkata, kalimatPertama, terms = processTXT(txt_file_words, searchQuery_vector, query_words_tunggal)
        #    terms = [list(item) for item in terms]
            if(len(terms) != 0): 
                hasil_internal.append((f[:len(f)-4], jumlahkata, kemiripan, kalimatPertama, 'internal_txt', terms))
 
    #proses semua html
    internal_html_path = os.path.join(basedir, 'static/uploads/html/')
    for f in listdir(internal_html_path):
        if(isfile(join(internal_html_path, f))):
            html = open(join(internal_html_path, f), encoding="utf8").read()
            #print(html)   
            soup = BeautifulSoup(html, 'html.parser')
            texts = []
 
            for i in soup.find_all('p'):
                texts.append(i.text)
            #print(texts)
            kemiripan, jumlahkata, kalimatPertama, terms = processTXT(" ".join(texts), searchQuery_vector, query_words_tunggal)
            #print(texts)
            if(len(terms) != 0): 
                hasil_internal.append((soup.title.string, jumlahkata, kemiripan, kalimatPertama, 'internal_html_' + join(f[:len(f)-5]), terms))
 #   print(hasil_internal)
    
    return hasil_internal

def cleanTheString(strings):
    #bersihkan dokumen terlebih dahulu dengan regex
    # print(strings)
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
    strings = strings.rstrip()

    after_cleaning = strings
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
    return hasil, after_cleaning
    
def mainSearch(searchQuery, externalDoc=""):
    #ubah queries menjadi vektor terlebih dahulu
    
    #bersihkan query, lakukan stemming, filtering (hapus stopwords)
    cleaned_query, _ = cleanTheString(searchQuery)
    
    vector_query = [i[1] for i in cleaned_query]
    query_words = [i[0] for i in cleaned_query]
    
#    print(query_words)
    search_result = []
#    print(vector_query)
#    print(query_words)
    #proses internal dokumen
    search_result += processInternal(vector_query, query_words)
    
    #proses external dokumen
    if(externalDoc != ""):
         search_result += processExternal(externalDoc, vector_query, query_words)

    x = lambda s : s[2]
    search_result.sort(reverse = True, key = x)        
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
#    mainSearch("tes satu dua")
    #print(htmlToStrings(html))
    #print(htmlToStrings("https://en.wikipedia.org/wiki/Computer_science"))
    #processExternal("https://en.wikipedia.org/wiki/Algorithm    https://en.wikipedia.org/wiki/Computer_science")
#    print("tes")
    #search_result, query_words, vec_terms = mainSearch("computer", "https://en.wikipedia.org/wiki/Algorithm    https://en.wikipedia.org/wiki/Computer_science")
    #print(search_result)
    from os.path import join, dirname, realpath
    file_path = join(join(join(dirname(realpath(__file__)), 'static/uploads/'), 'html'), 'mariana_ufo_incident_-_wikipedia.html')
    f = open(file_path)