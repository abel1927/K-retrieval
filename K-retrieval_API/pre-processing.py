import os
from typing import Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer #para  Back_formation(derivacion regresiva)
from nltk.stem import WordNetLemmatizer #para Lemmatisation_words(lematizacion)

from typing import List
import pandas as pd
import sklearn as sk
import math


def load_search(path:str):
    files = []
    dic={}
    ids=1
    for ruta, _ , archivos in os.walk(path, topdown=True):
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
        # freq = nltk.FreqDist(Lemmatisation_list)
        # for key,val in freq.items():
        #    print (str(key) + ':' + str(val))
        dic[ids]=(text[0],Lemmatisation_list)
        ids+=1
    return dic

def Preparation(dic2:Dict):
    all_document=[]
    for item in dic2.values():
        all_document.append(item[1])

    total=set(all_document[0])
    i=1

    while i <= all_document.__len__()-1 :
        total=total.union(all_document[i])
        i+=1

    i=all_document.__len__()
    lists_dir=[]
    while i>0:
        lists_dir.append(dict.fromkeys(total, 0))
        i-=1

    i=0
    for doc in all_document:
        for word in doc:
            lists_dir[i][word]+=1
        i+=1
    return lists_dir

def TF(wordDict):
    tfDict = {}
    corpusCount = max(wordDict.values().__iter__())
    for word, count in wordDict.items():
        tfDict[word] = count/float(corpusCount)
    return(tfDict)

def IDF(docList):
    import math
    idfDict = {}
    N = len(docList)
    
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))
        
    return idfDict 

def TFxIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return tfidf        
    
dic=load_search("E:/3ro Segundo Semestre/SRI/aqui")
dic1=remove_stopword(dic)
#Back_formation(dic1)
dic2=Lemmatisation_words(dic1)
lists_dir=Preparation(dic2)

list_tf=[]

for dic in lists_dir:
    list_tf.append(TF(dic))

tf = pd.DataFrame(list_tf)

idfs = IDF(lists_dir)

list_tfidf=[]
for item in list_tf:
    list_tfidf.append(TFxIDF(item, idfs))







       