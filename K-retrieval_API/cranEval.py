from typing import Dict
from index import Index
from vectorialIndex import VectorialIndex
from measures import *

class CranEval:

    def __init__(self, index:VectorialIndex, cranAll:str, cranQry:str, cranRel:str) -> None:
        self._index = index
        self._index.add_source(cranAll)
        self._queries = self.__load_Qry(cranQry=cranQry)
        self._rels = self.__load_Rel(cranRel=cranRel)
        self._retrieval_top20:Dict[int, list[str]] = {} # {query_id: top20}
        self._metrics:Dict[int, Dict[str,Dict[str,float]]] = {} # {q_id: {rank: {metric:value}}}

    def __load_Qry(self, cranQry:str) -> Dict[int, str]:
        _open=open(cranQry)
        _lines=_open.readlines()
        _open.close()
        queries:Dict[int,str] = {}
        i, n = 0, len(_lines)
        while i < n:
            queries[int(_lines[i])] = _lines[i+1]
            i+=2
        return queries
    
    def __load_Rel(self, cranRel:str) -> Dict[int, list[str]]:
        _open=open(cranRel)
        _lines=_open.readlines()
        _open.close()
        rels:Dict[int,list[str]] = {}
        for l in _lines:
            r = l.split()
            if rels.get(int(r[0])) == None:
                rels[int(r[0])] = []
            rels[int(r[0])].append(r[1])
        return rels

    def retrieval_all_query(self) -> None:
        for q_id, query in self._queries.items():
            self._retrieval_top20[q_id] = [ doc for doc,_ in self._index.get_rank(query=query)[0:20]]

    def get_metrics(self, queryId:int, top:int=20) -> Dict[str,float]:
        top = self._retrieval_top20[queryId][:top]
        relevants = self._rels[queryId]
        rt = len(relevants)
        rr, ri = 0, 0
        for r in top:
            if r[0:-4] in relevants:
                rr+=1
            else:
                ri+=1
        it = 1400 - rt
        metrics = {}
        p = precision(rr,ri) if rr+ri > 0 else 0
        rec = recovered(rr, rt) if rt > 0 else 0
        metrics['precision'] = p
        metrics['recall'] = rec
        metrics['Fpresicion'] = F(rr, ri, rt, beta=2) if (p!=0 and rec !=0) else 0
        metrics['Frecovered'] = F(rr, ri, rt, beta=0.5) if (p!=0 and rec !=0) else 0
        metrics['F1'] = F(rr, ri, rt) if (p!=0 and rec !=0) else 0
        metrics['fallout'] = fallaout(ri, it)
        return metrics

    def compute_all_queries_metrics(self, ranks:list[int]=[10,20]) -> Dict[int, Dict[str,Dict[str,float]]]:
        self._metrics = {}
        tops = [-1]
        tops.extend(ranks)
        for q_id, relevants in self._rels.items():
            self._metrics[q_id] = {}
            n_top = ""
            for top in tops:
                if top == -1:
                    top = len(relevants)
                    n_top = "Exact relevant top"
                else:
                    n_top = str(top)
                self._metrics[q_id][n_top] = self.get_metrics(queryId=q_id, top=top)
        return self._metrics

    def get_all_queries_metrics(self) -> Dict[str, Dict[int,Dict[str,float]]]:
        return self._metrics

    def get_Metric(self, metric:str):
        met:Dict[str,list[float]] = {}
        for _, ranks in self._metrics.items():
            for rank, metrics in ranks.items():
                if met.get(rank) == None:
                    met[rank] = []
                met[rank].append(metrics[metric])
        return met

