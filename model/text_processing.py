import os
from typing import Dict, Tuple, Callable
from nltk.corpus import stopwords
from nltk.tokenize import  wordpunct_tokenize
from nltk.stem import PorterStemmer 
from nltk.stem import WordNetLemmatizer 
import re
from .doc import Doc

def path_reader(path:str, start_id:int)->Tuple[Dict[int,Doc],Dict[int,str]]:
    dic_docs={}
    dic_text={}
    ids=  start_id
    for path, _ , files in os.walk(path, topdown=True):
        for doc in files:
            _open=open(path+'/'+doc)
            _read=_open.read()
            _open.close()
            name, extension = os.path.splitext(doc)
            name = name.removesuffix(extension)
            first_300 = _read[:300]
            first_300 = first_300+"..." if len(_read)>300 else first_300
            dic_docs[ids]= Doc(name, path+'/'+doc, first_300, extension)
            dic_text[ids] = _read
            ids+=1
    return (dic_docs, dic_text)

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
        """ Devuelve el texto expandiendo las contracciones 
        Ej can't ->  can not
        """
        text = re.sub(r"won\'t", "will not", text, re.IGNORECASE)
        text = re.sub(r"can\'t", "can not", text, re.IGNORECASE)
        text = re.sub(r"n\'t", " not", text)
        text = re.sub(r"\'re", " are", text)
        text = re.sub(r"\'s", " is", text)
        text = re.sub(r"\'d", " would", text)
        text = re.sub(r"\'ll", " will", text)
        text = re.sub(r"\'t", " not", text)
        text = re.sub(r"\'ve", " have", text)
        text = re.sub(r"\'m", " am", text)

        return text

    def only_alpha(self, text:str)->str:
        """ Elimina todas las cadenas no alfabéticas """
        text = re.sub(r"[^a-z]"," ", text)
        return re.sub(r" +", " ", text)

    def tokenizer_text(self, text:str)->list[str]:
        """ Devuelve la lista de tokens del texto """
        return wordpunct_tokenize(text)

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