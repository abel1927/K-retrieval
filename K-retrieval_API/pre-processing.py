import os
from typing import Dict
import textract
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer #para  Back_formation(derivacion regresiva)
from nltk.stem import WordNetLemmatizer #para Lemmatisation_words(lematizacion)


def load_search(path:str):
    files = []
    dic={}
    ids=1
    path1 ="E:/3ro Segundo Semestre/SRI/Nueva carpeta"
    for ruta, _ , archivos in os.walk(path1, topdown=True):
        for elemento in archivos:
            #if elemento.endswith((".txt", ".pdf", ".doc", ".docx")):
            if elemento.endswith((".txt")):
                _open=open(ruta+'/'+elemento)
                _read=_open.read()
                dic[ids]=(elemento,_read)
                ids+=1
    return dic

def remove_stopword(dic:Dict): 
    id=1
    dic_return={}
    for i in dic.values():
        dic_return[id]=(i[0],word_tokenize(i[1]))
        id+=1
    
    sr = stopwords.words('english')
    texts_tokens = list(dic_return.values())
    id=1

    for text in texts_tokens:

        for token in text[1]:
            if token in sr :
                text[1].remove(token)
        dic_return[id]=(text[0],text[1])
        id+=1
    
    return dic_return

def Back_formation(dic:Dict):
    stemmer = PorterStemmer()
    ids=1
    for text in dic.values():
        back_list=[]
        for token in text[1]:  

            back_list.append(stemmer.stem(token))
        dic[ids]=(text[0],back_list)
        ids+=1
    return dic

def Lemmatisation_words(dic:Dict):
    lemmatizer = WordNetLemmatizer()
    ids=1
    for text in dic.values():
        Lemmatisation_list=[]
        for token in text[1]:  
            Lemmatisation_list.append(lemmatizer.lemmatize(token))
        dic[ids]=(text[0],Lemmatisation_list)
        ids+=1
    return dic

        
    
dic=load_search("E:/3ro Segundo Semestre/SRI/Nueva carpeta")
dic1=remove_stopword(dic)
Back_formation(dic1)
Lemmatisation_words(dic1)




       