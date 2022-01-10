import os
from typing import Dict
import textract
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
            _read = None
            if elemento.endswith((".PDF", ".pdf")):
                _read = textract.process(ruta+'/'+elemento)
            else:#si es .txt
                _open=open(ruta+'/'+elemento)
                _read=_open.read()
                dic[ids]=(elemento,_read)
                ids+=1
        # for elemento in archivos:
        #     #if elemento.endswith((".txt", ".pdf", ".doc", ".docx")):
        #     if elemento.endswith((".txt")):
        #         _open=open(ruta+'/'+elemento)
        #         _read=_open.read()
        #         dic[ids]=(elemento,_read)
        #         ids+=1
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

def Preparation(list_doc):
    

    total=set(list_doc[0][1])
    i=1

    while i <= list_doc.__len__()-1 :
        total=total.union(list_doc[i][1])
        i+=1

    j=list_doc.__len__()
    lists_dir=[]
    i=0
    while i<j:
        lists_dir.append((list_doc[i][0], dict.fromkeys(total, 0)))
        i+=1

    i=0
    for doc in list_doc:
        for word in doc[1]:
            lists_dir[i][1][word]+=1
        i+=1
    return lists_dir

def TF(wordDict):
    tfDict = {}
    corpusCount = max(wordDict[1].values().__iter__())
    for word, count in wordDict[1].items():
        tfDict[word] = count/float(corpusCount)
    return(tfDict)

def IDF(docList):
    import math
    idfDict = {}
    N = len(docList)
    
    idfDict = dict.fromkeys(docList[0][1].keys(), 0)
    for doc in docList:
        for word, val in doc[1].items():
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

list_doc=[]
for id, item in dic2.items():
    t=(id,item[1])
    list_doc.append(t)

lists_dir=Preparation(list_doc)

list_tf=[]
for dic in lists_dir:
    list_tf.append((dic[0],TF(dic)))

idfs = IDF(lists_dir)

list_tfidf=[]
for item in list_tf:
    list_tfidf.append((item[0], TFxIDF(item[1], idfs)))


######------------------------------Processing query

def remove_stopword_query(query): 
    query_list=word_tokenize(query)
    sr = stopwords.words('english')

    for token in query_list:
        if token in sr :
            query_list.remove(token)
    
    return query_list



def Lemmatisation_words_query(query_list):

    lemmatizer = WordNetLemmatizer()
    Lemmatisation_list=[]

    for token in query_list:  
        Lemmatisation_list.append(lemmatizer.lemmatize(token))
    
    return Lemmatisation_list


def Preparation_query(document_terms,query_list):
    i=query_list.__len__()
    lists_dir=dict.fromkeys(document_terms, 0)

    i=0
    for word in query_list:
        lists_dir[word]+=1
    i+=1
    return lists_dir

def TF_query(wordDict):
    tfDict = {}
    corpusCount = max(wordDict.values().__iter__())
    for word, count in wordDict.items():
        tfDict[word] = count/float(corpusCount)
    return(tfDict)



def TFxIDF_query(tfBow, idfs,a):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = (a+(1-a)*val)*idfs[word]
    return tfidf   



def Similarity(query, doc):
     vecResult1=multiply(query,doc)
     numerator=0
     for item in vecResult1:
         numerator+=item
     doc2=math.sqrt(Pow(doc)) 
     query2=math.sqrt(Pow(query)) 
     denominator=doc2*query2
     return  numerator/denominator

def Pow(vec):
    resul=0
    for item in vec.values():
        resul+=pow(item,2)
    return resul



def multiply(vec1, vec2):
    mult=[]
    for word, val in vec1.items():
        mult.append(val*vec2[word])
    return mult

 
        

query="leon zorro"#------------------------------ABEL HAY QUE PASARLE LA QUERY--------------
query_list=remove_stopword_query(query)
Lemmatisation_list=Lemmatisation_words_query(query_list)

total=set(list_doc[0][1])
i=1
while i <= list_doc.__len__()-1 :
    total=total.union(list_doc[i][1])
    i+=1

lists_dir=Preparation_query(total,Lemmatisation_list)

dic_tf=TF_query(lists_dir)

queryW=TFxIDF_query(dic_tf, idfs,0.4)

similitud=[]
for doc in list_tfidf:
    similitud.append((doc[0],Similarity(queryW,doc[1])))

similitud.sort(key = lambda x: x[1], reverse=True)
 







       