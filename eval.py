from typing import Dict
from matplotlib import pyplot as plt
from model.measures import *
from model.index import Index
from model.text_processing import TextProcessor
from model.vectrorialIndex import VectorialIndex
from time import time

def __load_Keys(key:str) -> Dict[int, list[int]]:
    _open=open(key)
    _lines=_open.readlines()
    _open.close()
    keys:Dict[int,list[int]] = {}
    for l in _lines:
        r = l.split()
        if keys.get(int(r[0])) == None:
            keys[int(r[0])] = []
        keys[int(r[0])].append(int(r[1]))
    return keys

def __load_Qry(qry:str) -> Dict[int, str]:
    _open=open(qry)
    _lines=_open.readlines()
    _open.close()
    queries:Dict[int,str] = {}
    i, n = 0, len(_lines)
    while i < n:
        queries[int(_lines[i])] = _lines[i+1]
        i+=2
    return queries

def time_test(source:str, index:Index, rep:int=10)-> float:
    total = 0
    for _ in range(rep):
        start = time()
        index.add_source(source)
        end = time()
        total+=end-start
        index.clean()
    return round(total/rep,4)


def save_retrieval_all_query(Index:Index, Qry:str, response_path:str, rank:int=40)->None:
    file = open(response_path, 'w')
    queries = __load_Qry(Qry)
    for q_id, query in queries.items():
        for d, sim in Index.get_rank(query=query)[:rank]:
            file.write(f"{q_id} {d.name()} {sim}\n")
    file.close()

def get_metrics(relevants:set[int], responses:set[int], docs_total:int):
    r = len(responses)
    rr = len(responses.intersection(relevants))
    ri = r-rr
    rt = min(len(relevants),r)
    it = docs_total - rt
    p = precision(rr,ri) if rr+ri > 0 else 0
    rec = recall(rr, rt) if rt > 0 else 0
    f1 = F(rr, ri, rt) if (p!=0 and rec !=0) else 0
    fall = fallaout(ri, it)
    return (p, rec, f1, fall)

def plot(y_label:str, xlabel:str,suptitle:str, vals:list, color:str, save:bool):
    fig, ax = plt.subplots()
    ax.set_ylabel(y_label)
    ax.set_xlabel(xlabel)
    fig.suptitle(suptitle, fontsize=15)
    plt.hist(vals,color=color)
    plt.show()
    if save:
        fig.savefig(f'{suptitle}.png')

def generate_response(save_response_path:str, all_path:str, qry_path:str, rank=40):
    index = VectorialIndex()
    index.add_source(all_path)
    save_retrieval_all_query(index, qry_path, save_response_path, rank=rank)

def metrics_by_rank(rels:str, res:str, docs_total:int,
        ranks=[-1,5,10,20,40], ploting:bool=False, save:bool=False):
    q_relevants = __load_Keys(rels)
    q_top20 = __load_Keys(res)
    n_top = ""
    for top in ranks:
        if top == -1:
            n_top = "R-metric"
            print(n_top)
        else:
            n_top = f"Top-{str(top)} metric"
            print(n_top)
        print('--------------------------------')
        precisions, recalls, f1, fallouts = [],[],[],[]
        map = 0
        for q_id, relevants in q_relevants.items():
            rank = top
            if top == -1:
                rank = len(relevants)
            map += avg_precision(relevants, q_top20[q_id][:rank])
            p,r,f,fall = get_metrics(set(relevants), set(q_top20[q_id][:rank]), docs_total)
            precisions.append(p)
            recalls.append(r)
            f1.append(f)
            fallouts.append(fall)
        if ploting:
            plot('#queries', 'Precision', f'Presicion {n_top}', vals=precisions, color='mediumblue', save=save)
        print(f"Average Precision {n_top}: {round(sum(precisions)/len(precisions),4)}")

        print(f"Mean Average Precision {n_top}: {round(map/len(q_relevants),4)}")

        if ploting:
            plot('#queries', 'Recall', f'Recall {n_top}', vals=f1, color='indigo', save=save)
        print(f"Average Recall {n_top}: {round(sum(recalls)/len(recalls),4)}")

        if ploting:
            plot('#queries', 'F1', f'F1 {n_top}', vals=f1, color='darkcyan', save=save)
        print(f"Average F1 {n_top}: {round(sum(f1)/len(f1),4)}")

        if ploting:
            plot('#queries', 'Fallout', f'Fallaout {n_top}', vals=fallouts, color='darkmagenta', save=save)
        print(f"Average Follout {n_top}: {round(sum(fallouts)/len(fallouts),4)}")

        print('\n')

        if ploting:
            fig, ax = plt.subplots()
            ax.set_ylabel('recall')
            ax.set_xlabel('precision')
            fig.suptitle(f'Recall-Precision {n_top}', fontsize=15)
            plt.scatter(precisions, recalls, s=44, color='cadetblue', alpha=0.6)
            plt.show()
            if save:
                fig.savefig(f'Recall-Precision {n_top}.png')

#select your locals path

cranAll = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/cranAll/"
cranQry = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/cranQry.txt"
cranRel = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/cranqrel"

cisiAll = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cisi/cisi docs/"
cisiQry = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cisi/cisiQuery.txt"
cisiRel = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cisi/CISI.REL"

nlpAll = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/nlp/nlp docs/"
nlpQry = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/nlp/nlpQuery.txt"
nlpRel = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/nlp/nlpRel.txt"

#----Descomentar esta seccion para correr los test de tiempo  -----------#
#
#print(f"Cran Indexed time: {time_test(cranAll, VectorialIndex(), 100)}")
#print(f"Cisi Indexed time: {time_test(cisiAll, VectorialIndex(), 100)}")
#print(f"Nlp Indexed time: {time_test(nlpAll, VectorialIndex(), 100)}")
#
#----------

#----Descomentar esta seccion para crear un nuevo response -----------#
#
#cranSaveResponse = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/response/cran_response.txt"
#generate_response(cranSaveResponse, cranAll, cranQry)

#cisiSaveResponse = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cisi/response/cisi_response.txt"
#generate_response(cisiSaveResponse, cisiAll, cisiQry, rank=175)

#nlpSaveResponse = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/nlp/response/nlp_response.txt"
#generate_response(nlpSaveResponse, nlpAll, nlpQry)

#------------


#----Descomentar esta seccion para obtener las metricas -----------#

#Cran Metrics
#cranLoadResponse = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/response/cran_response.txt"
#metrics_by_rank(cranRel, cranLoadResponse, docs_total=1400, ploting=False, save=True)

#Cisi Metrics
#cisiLoadResponse = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cisi/response/cisi_response.txt"
#metrics_by_rank(cisiRel, cisiLoadResponse, docs_total=1460, ploting=False, save=True)

#Nlp Metrics
#nlpLoadResponse = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/nlp/response/nlp_response.txt"
#metrics_by_rank(nlpRel, nlpLoadResponse, docs_total=11429, ploting=False, save=True)
