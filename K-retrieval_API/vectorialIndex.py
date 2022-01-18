from typing import Dict
from index import Index
from text_processing import TextProcessor, path_reader
from vectorization import Vectorizer
from vector_utils import similarity

no_terms = [' ', '.', ',', '!', '/', '(', ')', '?', ';', ':', 
        '...', "'", """""""", "”", "’", "“"]

class VectorialIndex(Index):

    def __init__(self, 
    textProcessor:TextProcessor = TextProcessor(), vectorizer:Vectorizer = Vectorizer()) -> None:
        super().__init__()
        self._sources = []
        self._documents:Dict[int,str] = {} # {id:name}
        self._documentsText:Dict[int,str] = {} # {id:text}
        self._documentsTokens:Dict[int,list[str]] = {} #{id: tokens}
        self._words_count:Dict[int,Dict[str,int]] = {} # {id : {word:count}}
        self._words_TF:Dict[int, Dict[str,float]] = {} # {id : {word:tf}}
        self._words_IDF:Dict[str,float] = {} # {word:idf}
        self._words_TFxIDF:Dict[int, Dict[str,float]] = {} # {id : {word:tfxidf}}
        self._all_words:set[str] = set()
        self._textProcessor = textProcessor
        self._vectorizer = vectorizer
        self._last_index = 0


    def add_source(self, new_path:str)-> None:
        """ Indexa los documentos presentes en new_path"""
        new_last_index, dict_name, dict_docs = path_reader(new_path, self._last_index+1)
        self._documents.update(dict_name)
        self._documentsText.update(dict_docs)
        ids:list[int] = []
        tokens_list:list[list[str]] = []
        for id, text in dict_docs.items():
            exp_text = self._textProcessor.expand_text(text.lower())
            tokens = self._textProcessor.tokenizer_text(text=exp_text)
            nst_tokens = self._textProcessor.remove_non_important_terms(tokens=tokens)
            norm_tokens = self._textProcessor.normalizer(nst_tokens)
            self._documentsTokens[id] = norm_tokens
            ids.append(id)
            tokens_list.append(norm_tokens)
        new_words = self._vectorizer.words_extraction(tokens_list)
        self._all_words = self._all_words.union(new_words)
        for id, word_count in self._words_count.items():
            self._words_count[id] = dict.fromkeys(self._all_words, 0).update(word_count)
        for i in range(len(ids)):
            self._words_count[ids[i]] = self._vectorizer.words_count(self._all_words, tokens_list[i])
        for id, word_tf in self._words_TF.items():
            self._words_TF[id] = dict.fromkeys(self._all_words, 0).update(word_tf)
        for i in range(len(ids)):
            self._words_TF[ids[i]] = self._vectorizer.TF(self._words_count[ids[i]])
        self._words_IDF = self._vectorizer.IDF(self._all_words, list(self._documentsTokens.values()))
        for id, words_tf in self._words_TF.items():
            self._words_TFxIDF[id] = self._vectorizer.TFxIDF(words_tf, self._words_IDF)
        self._last_index = new_last_index
        self._sources.append(new_path)

    def get_rank(self, query:str) -> list:
        """ Devuelve los resultados relevantes para la consulta"""
        rank = []
        exp_q = self._textProcessor.expand_text(query.lower())
        tokens = self._textProcessor.tokenizer_text(text=exp_q)
        nst_tokens = self._textProcessor.remove_non_important_terms(tokens=tokens)
        q_tokens = self._textProcessor.normalizer(nst_tokens)
        q_count = self._vectorizer.words_count(self._all_words, [q for q in q_tokens if q in self._all_words])
        if max(q_count.values().__iter__()) == 0:
            return rank
        q_tf = self._vectorizer.TF(q_count)
        q_TFxIDF = self._vectorizer.TFxIDF(q_tf, self._words_IDF, a=0)
        q_vec = list(q_TFxIDF.values())
        for id, word_TFxIDF in self._words_TFxIDF.items():
            rank.append((self._documents[id], similarity(list(word_TFxIDF.values()), query_vec=q_vec)))
        rank.sort(key = lambda x: x[1], reverse=True)
        return rank


    def get_indexed_terms_count(self) -> int:
        """ Devuelve la cantidad de términos indexados"""
        return len(self._all_words)

    def get_indexed_docs_count(self) -> int:
        """ Devuelve la cantidad de documentos indexados"""
        return self._last_index

    def get_indexed_terms(self) -> list[str]:
        """ Devuelve la lista de términos indexados"""
        return list(self._all_words)

    def get_indexed_docs(self) -> list[str]:
        """ Devuelve la lista de documentos indexados"""
        return list(self._documents.values())

    def clean(self):
        """ Vacía la colección"""
        self._sources = []
        self._documents:Dict[int,str] = {} # {id:name}
        self._documentsText:Dict[int,str] = {} # {id:text}
        self._documentsTokens:Dict[int,list[str]] = {} #{id: tokens}
        self._words_count:Dict[int,Dict[str,int]] = {} # {id : {word:count}}
        self._words_TF:Dict[int, Dict[str,float]] = {} # {id : {word:tf}}
        self._words_IDF:Dict[str,float] = {} # {word:idf}
        self._words_TFxIDF:Dict[int, Dict[str,float]] = {} # {id : {word:tfxidf}}
        self._all_words:set[str] = set()
        self._last_index = 0

