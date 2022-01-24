from typing import Dict
from math import log10

def words_extraction(collection:list[list[str]])-> set[str]:
    s = None
    if len(collection) > 0:
        s = set(collection[0])
        for texts in  collection:
            s = s.union(texts)
    return s

def words_count(all_words:set[str], document_words:list[str])-> Dict[str,int]:
    words_count = dict.fromkeys(all_words, 0)
    for word in document_words:
        words_count[word]+=1
    return words_count

def TF(words_count:Dict[str,int]) -> Dict[str,float]:
    max_count = max(words_count.values().__iter__())
    tfDict = {}
    for word, count in words_count.items():
        if max_count == 0:
            tfDict[word] = 0
        else:
            tfDict[word] = count/float(max_count)
    return tfDict

def IDF(all_words:set[str], collection:list[list[str]]) -> Dict[str,float]:
    N = len(collection)
    idfDict = dict.fromkeys(all_words, 0)
    for word in all_words:
        for text in collection:
            if word in text:
                idfDict[word]+=1
        idfDict[word] = log10(N / float(idfDict[word]))
    return idfDict

def TFxIDF(tfdict:Dict[str,float], idfDict:Dict[str,float], a:float = 0)->Dict[str,float]:
    tfIdf = {}
    for word, tf in tfdict.items():
        tfIdf[word] = (a+(1-a)*tf)*idfDict[word]
    return tfIdf
