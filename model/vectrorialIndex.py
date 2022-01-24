from typing import Dict
from .index import Index
from math import log10
from .text_processing import TextProcessor, path_reader
from .vectorization import *
from .doc import Doc
from time import time

class VectorialIndex(Index):

    def __init__(self, 
    textProcessor:TextProcessor = TextProcessor()) -> None:
        super().__init__()
        self._acc_index_time = 0
        self._sources = []                               # list of indexed paths 
        self._documents:Dict[int,Doc] = {}               # {doc_id: Doc}
        self._textProcessor = textProcessor              # 
        self._idf:Dict[str,float] = {}                   #
        self._index:Dict[str,Dict[int,list[float]]] = {} # {term: {doc_id: (tf,w)}}

    def add_source(self, source_path:str)-> int:
        start = time()
        N_old = len(self._documents)
        dict_docs, dict_text = path_reader(source_path, N_old)
        document_tokens:Dict[int,list[str]] = {}
        N_news = len(dict_docs)
        N = N_news + N_old
        for id, text in dict_text.items():
            exp_text = self._textProcessor.expand_text(text.lower())
            alpha_t = self._textProcessor.only_alpha(exp_text)
            tokens = self._textProcessor.tokenizer_text(text=alpha_t)
            nst_tokens = self._textProcessor.remove_non_important_terms(tokens=tokens)
            norm_tokens = self._textProcessor.normalizer(nst_tokens)
            document_tokens[id] = norm_tokens
        index:Dict[str,Dict[int,list[float]]] = {}
        max_freq_doc = [0]*N_news
        for id, tokens in document_tokens.items():
            for token in tokens:
                if index.get(token) == None:
                    index[token] = {}
                if index[token].get(id) == None:
                    index[token][id] = [0,0]
                index[token][id][0]+=1 
                if index[token][id][0] > max_freq_doc[id-N_old]:
                    max_freq_doc[id-N_old] = index[token][id][0]
        for t, docs_f in index.items():
            for doc_id, freq_0 in docs_f.items():
                index[t][doc_id][0]  = freq_0[0]/max_freq_doc[doc_id-N_old]
        idf:Dict[str,float] = {}
        all_words = set(list(self._index.keys()))
        all_words =  all_words.union(set(list(index.keys())))
        for t in all_words:
            if self._index.get(t) != None and index.get(t) != None:
                idf[t] = log10(N/(len(self._index[t])+len(index[t])))
                self._index[t].update(index[t])
            elif index.get(t) != None:
                idf[t] = log10(N/len(index[t]))
                self._index[t] = index[t]
            else:
                idf[t] = log10(N/len(self._index[t]))
        for t, docs_f in self._index.items():
            for doc_id, tf_w in docs_f.items():
                self._index[t][doc_id][1]  = tf_w[0]*idf[t]
        self._idf = idf
        self._documents.update(dict_docs)
        self._sources.append(source_path)
        end = time()
        self._acc_index_time += end-start
        return N_news

    def get_rank(self, query:str) -> list:
        """ Devuelve los resultados relevantes para la consulta"""
        rank:list[float] = []
        exp_q = self._textProcessor.expand_text(query.lower())
        alpha_t = self._textProcessor.only_alpha(exp_q)
        tokens = self._textProcessor.tokenizer_text(text=alpha_t)
        nst_tokens = self._textProcessor.remove_non_important_terms(tokens=tokens)
        q_tokens = self._textProcessor.normalizer(nst_tokens)
        _all_words = set(self._index.keys())
        q_count = words_count(_all_words, [q for q in q_tokens if q in _all_words])
        if max(q_count.values().__iter__()) == 0:
            return rank
        rank = [0]*len(self._documents)
        length = [0]*len(self._documents)
        q_tf = TF(q_count)
        q_w = TFxIDF(q_tf, self._idf, a=0)
        Wq = 0
        for t, w in q_w.items():
            if w == 0:
                continue
            Wq+= w**2
            for doc_id, tf_tfidf in self._index[t].items():
                rank[doc_id]+= w*tf_tfidf[1]
        Wq = Wq**(1/2)
        for t, doc_tfidf in self._index.items():
            for doc_id, tf_tfidf in doc_tfidf.items():
                length[doc_id]+=tf_tfidf[1]**2
        length = [(k**(1/2))*Wq for k in length]
        for d in range(len(rank)):
            rank[d] = rank[d]/length[d] if length[d]!=0 else 0
        return [(self._documents[key], score) for score, key in sorted(zip(rank,list(self._documents.keys())), reverse=True) if score != 0]

    def get_sources(self) -> list[str]:
        """ Devuelve las rutas presentes en la colección"""
        return self._sources

    def get_indexed_terms_count(self) -> int:
        """ Devuelve la cantidad de términos indexados"""
        return len(self._index)

    def get_indexed_docs_count(self) -> int:
        """ Devuelve la cantidad de documentos indexados"""
        return len(self._documents)

    def get_indexed_terms(self) -> list[str]:
        """ Devuelve la lista de términos indexados"""
        return list(self._index.keys())

    def get_indexed_docs(self) -> list[str]:
        """ Devuelve la lista de documentos indexados"""
        return list(self._documents.values())

    def clean(self):
        """ Vacía la colección"""
        self._acc_index_time = 0
        self._documents:Dict[int,str] = {} 
        self._idf:Dict[str,float] = {}
        self._sources:list[str] = []
        self._index:Dict[str,Dict[int,list[float]]] = {}

    def get_stats(self) -> Dict:
        """ 
        Devuelve estadisticas de la colección 
        {"total terms" : int,
        "total docs"   : int,
        'total sorces' : int,
        "most present terms" : list[(str,int)]
        "idfs" : idfvalues,
        "indexed time/doc" : str}
        """
        stats = {}
        t_docs = self.get_indexed_terms_count()
        stats['total terms'] = t_docs
        stats['total docs'] = self.get_indexed_docs_count()
        stats['total sorces'] = len(self._sources)
        more_present_terms = [(t,len(docs)) for t, docs in self._index.items()]
        more_present_terms.sort(key = lambda x: x[1], reverse=True)
        stats['most present terms'] = more_present_terms[:10]
        stats['idfs'] = list(self._idf.values())
        
        stats['indexed time/doc'] = round(self._acc_index_time/t_docs,4) if t_docs > 0 else '-'
        return stats
