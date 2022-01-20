from typing import Dict
from index import Index
from math import log10
from text_processing import TextProcessor, path_reader
from vectorization import Vectorizer

from pprint import pprint

class VectorialIndex(Index):

    def __init__(self, 
    textProcessor:TextProcessor = TextProcessor(), vectorizer:Vectorizer = Vectorizer()) -> None:
        super().__init__()
        #self._sources = []
        self._documents:Dict[int,str] = {} # {id:name}
        self._textProcessor = textProcessor
        self._vectorizer = vectorizer
        self._idf:Dict[str,float] = {}
        self._postingList:Dict[str,Dict[int,float]] = {}


    def add_source(self, new_path:str)-> None:
        dict_name, dict_docs = path_reader(new_path)
        document_tokens:Dict[int,list[str]] = {}
        N = len(dict_name)
        for id, text in dict_docs.items():
            exp_text = self._textProcessor.expand_text(text.lower())
            alpha_t = self._textProcessor.only_alpha(exp_text)
            tokens = self._textProcessor.tokenizer_text(text=alpha_t)
            nst_tokens = self._textProcessor.remove_non_important_terms(tokens=tokens)
            norm_tokens = self._textProcessor.normalizer(nst_tokens)
            document_tokens[id] = norm_tokens
        index:Dict[str,Dict[int,float]] = {}
        max_freq_doc = [0]*N
        for id, tokens in document_tokens.items():
            for token in tokens:
                if index.get(token) == None:
                    index[token] = {}
                if index[token].get(id) == None:
                    index[token][id] = 0
                index[token][id]+=1
                if index[token][id] > max_freq_doc[id]:
                    max_freq_doc[id] = index[token][id]
        for t, docs_f in index.items():
            for doc_id, freq in docs_f.items():
                index[t][doc_id]  = freq/max_freq_doc[doc_id]
        idf:Dict[str,float] = {}
        for t , docs_f in index.items():
            idf[t] = log10(N/len(docs_f))
        for t, docs_f in index.items():
            for doc_id, tf in docs_f.items():
                index[t][doc_id]  = tf*idf[t]
        self._postingList = index
        self._idf = idf
        self._documents = dict_name
        pprint(idf)


    def get_rank(self, query:str) -> list:
        """ Devuelve los resultados relevantes para la consulta"""
        rank = []
        exp_q = self._textProcessor.expand_text(query.lower())
        alpha_t = self._textProcessor.only_alpha(exp_q)
        tokens = self._textProcessor.tokenizer_text(text=alpha_t)
        nst_tokens = self._textProcessor.remove_non_important_terms(tokens=tokens)
        q_tokens = self._textProcessor.normalizer(nst_tokens)
        _all_words = set(self._postingList.keys())
        q_count = self._vectorizer.words_count(_all_words, [q for q in q_tokens if q in _all_words])
        if max(q_count.values().__iter__()) == 0:
            return rank
        rank = [0]*len(self._documents)
        length = [0]*len(self._documents)
        q_tf = self._vectorizer.TF(q_count)
        q_w = self._vectorizer.TFxIDF(q_tf, self._idf, a=0)

        #pprint([(i,j) for i,j in q_w.items() if j != 0])
        Wq = 0
        for t, w in q_w.items():
            if w == 0:
                continue
            Wq+= w**2
            for doc_id, tfidf in self._postingList[t].items():
                rank[doc_id]+= w*tfidf
        Wq = Wq**(1/2)
        for t, doc_tfidf in self._postingList.items():
            for doc_id, tfidf in doc_tfidf.items():
                length[doc_id]+=tfidf**2
        length = [(k**(1/2))*Wq for k in length]
        for d in range(len(rank)):
            rank[d] = rank[d]/length[d] if length[d]!=0 else 0
        return  [(doc, score) for score, doc in sorted(zip(rank,list(self._documents.values())), reverse=True)]

    def get_indexed_terms_count(self) -> int:
        """ Devuelve la cantidad de términos indexados"""
        return len(self._postingList)

    def get_indexed_docs_count(self) -> int:
        """ Devuelve la cantidad de documentos indexados"""
        return len(self._documents)

    def get_indexed_terms(self) -> list[str]:
        """ Devuelve la lista de términos indexados"""
        return list(self._postingList.keys())

    def get_indexed_docs(self) -> list[str]:
        """ Devuelve la lista de documentos indexados"""
        return list(self._documents.values())

    def clean(self):
        """ Vacía la colección"""
        self._documents:Dict[int,str] = {} # {id:name}
        self._idf:Dict[str,float] = {}
        self._postingList:Dict[str,Dict[int,float]] = {}
