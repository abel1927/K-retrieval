from typing import Dict
from matplotlib import pyplot as plt
from measures import *
from index import Index
from text_processing import TextProcessor, no_terms
from vectrorialIndex import VectorialIndex

def __load_Keys(cranKey:str) -> Dict[int, list[int]]:
    _open=open(cranKey)
    _lines=_open.readlines()
    _open.close()
    keys:Dict[int,list[int]] = {}
    for l in _lines:
        r = l.split()
        if keys.get(int(r[0])) == None:
            keys[int(r[0])] = []
        keys[int(r[0])].append(int(r[1]))
    return keys

def __load_Qry(cranQry:str) -> Dict[int, str]:
    _open=open(cranQry)
    _lines=_open.readlines()
    _open.close()
    queries:Dict[int,str] = {}
    i, n = 0, len(_lines)
    while i < n:
        queries[int(_lines[i])] = _lines[i+1]
        i+=2
    return queries

def save_retrieval_all_query(cranIndex:Index, cranQry:str, response_path:str, rank:int=40)->None:
    file = open(response_path, 'w')
    queries = __load_Qry(cranQry)
    for q_id, query in queries.items():
        for d, sim in cranIndex.get_rank(query=query)[:rank]:
            file.write(f"{q_id} {d[:-4]} {sim}\n")
    file.close()

def get_metrics(relevants:set[int], responses:set[int]):
    r = len(responses)
    rr = len(responses.intersection(relevants))
    ri = r-rr
    rt = len(relevants)
    it = 1400 - rt
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

def metrics_by_rank(cranRel:str, cranRes:str, ranks=[-1,10,20,40], ploting:bool=False, save:bool=False):
    q_relevants = __load_Keys(cranRel)
    q_top20 = __load_Keys(cranRes)

    n_top = ""
    for top in ranks:
        if top == -1:
            n_top = "K-metric"
            print(n_top)
        else:
            n_top = f"Top-{str(top)} metric"
            print(n_top)
        print('--------------------------------')
        precisions, recalls, f1, fallouts = [],[],[],[]
        for q_id, relevants in q_relevants.items():
            rank = top
            if top == -1:
                rank = len(relevants)
            p,r,f,fall = get_metrics(set(relevants), set(q_top20[q_id][:rank]))
            precisions.append(p)
            recalls.append(r)
            f1.append(f)
            fallouts.append(fall)
        if ploting:
            plot('#queries', 'Precision', f'Presicion {n_top}', vals=precisions, color='mediumblue', save=save)
        print(f"Precision promedio {n_top}: {round(sum(precisions)/len(precisions),4)}")

        if ploting:
            plot('#queries', 'Recall', f'Recall {n_top}', vals=f1, color='indigo', save=save)
        print(f"Recall promedio {n_top}: {round(sum(recalls)/len(recalls),4)}")

        if ploting:
            plot('#queries', 'F1', f'F1 {n_top}', vals=f1, color='darkcyan', save=save)
        print(f"F1 promedio {n_top}: {round(sum(f1)/len(f1),4)}")

        if ploting:
            plot('#queries', 'Fallout', f'Fallaout {n_top}', vals=fallouts, color='darkmagenta', save=save)
        print(f"Follout promedio {n_top}: {round(sum(fallouts)/len(fallouts),4)}")

        print('\n')

        if plot:
            fig, ax = plt.subplots()
            ax.set_ylabel('recall')
            ax.set_xlabel('precision')
            fig.suptitle(f'Recall-Precision {n_top}', fontsize=15)
            plt.scatter(precisions, recalls, s=44, color='cadetblue', alpha=0.6)
            plt.show()
            if save:
                fig.savefig(f'Recall-Precision {n_top}.png')

#select your locals path
cranAll_path = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/cranAll/"
cranQry_path = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/cranQry.txt"
cranRel_path = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/cranqrel"

#----Descomentar esta seccion para crear un nuevo response -----------#
#
cranSaveResponse_path = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/response/response3.txt"
cranIndex = VectorialIndex(textProcessor=TextProcessor(unnused_characters=no_terms))
cranIndex.add_source(cranAll_path)
save_retrieval_all_query(cranIndex, cranQry_path, cranSaveResponse_path)
#
#-------

#----Descomentar esta seccion para obtener las metricas response -----------#

cranLoadResponse_path = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/response/response3.txt"
metrics_by_rank(cranRel_path, cranLoadResponse_path, ploting=True, save=True)

