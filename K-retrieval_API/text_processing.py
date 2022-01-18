import os
from typing import Dict, Tuple, Callable
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from nltk.stem import PorterStemmer 
from nltk.stem import WordNetLemmatizer 
import re

def path_reader(path:str, initial_id:int = 0)->Tuple[int,Dict[int,str],Dict[int,str]]:
    dic_name={}
    dic_text={}
    ids=initial_id
    for ruta, _ , archivos in os.walk(path, topdown=True):
        for elemento in archivos:
            _open=open(ruta+'/'+elemento)
            _read=_open.read()
            _open.close()
            dic_name[ids]=elemento 
            dic_text[ids] = _read
            ids+=1
    return (ids, dic_name, dic_text)

no_terms = [' ', '.', ',', '!', '/', '(', ')', '?', ';', ':', 
        '...', "'", """""""", "”", "’", "“"]

class TextProcessor:

    def __init__(self, unnused_characters:list[str] = []) -> None:
        self._stop_words:list[str] = stopwords.words('english')
        self._stop_words.extend(unnused_characters)
        self._stemmer = None
        self._lemmatizer = None

    def add_unnused_characters(self, unnused_characters:list[str])->None:
        self._stop_words.extend(unnused_characters)

    def expand_text(self,text:str)-> str:
        text = re.sub(r"won\'t", "will not", text, re.IGNORECASE)
        text = re.sub(r"can\'t", "can not", text, re.IGNORECASE)
    
        # general
        text = re.sub(r"n\'t", " not", text)
        text = re.sub(r"\'re", " are", text)
        text = re.sub(r"\'s", " is", text)
        text = re.sub(r"\'d", " would", text)
        text = re.sub(r"\'ll", " will", text)
        text = re.sub(r"\'t", " not", text)
        text = re.sub(r"\'ve", " have", text)
        text = re.sub(r"\'m", " am", text)

        text = re.sub(r"[\'#\(\)/.,;:?$%!&*^]+", " ", text)
        return text

    def tokenizer_text(self, text:str)->list[str]:
        return wordpunct_tokenize(text)
        #return word_tokenize(text)

    def remove_non_important_terms(self, tokens:list[str])->list[str]:
        without = []
        for token in tokens:
            if not token in self._stop_words:
                without.append(token)
        return without
    
    def normalizer(self, words:list[str], 
    method:str = 'l', other_method:Callable[[str],str]=None)->list[str]:
        """
        Normaliza los términos utilizando el método seleccionado en el parámeto 'method'.
        Si no se incluye el parámeto 'method' o es un valor incorrecto se utiliza el 
        por defecto el método de WordNetLemmatizer.
        Si se recibe el parámetro 'other_method' se utiliza este para la normalización sin 
        importat el valor en 'method' 
        .method:
            -["s", "stem", "porter"] -> PorterStemmer method
            -["l", "lemmatize", "lemma", "wordnet"] -> WordNetLemmatizer method
        """
        normalized = []
        if other_method != None:
            for w in words:
                normalized.append(other_method(w))
        elif method.lower() in ["s", "stem", "porter"]:
            if self._stemmer == None:
                self._stemmer = PorterStemmer()
            for w in words:
                normalized.append(self._stemmer.stem(w))
        else:
            if self._lemmatizer == None:
                self._lemmatizer = WordNetLemmatizer()
            for w in words:
                normalized.append(self._lemmatizer.lemmatize(w))
        return normalized

