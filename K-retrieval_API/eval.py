from index import Index
from vectorialIndex import VectorialIndex
from text_processing import TextProcessor, no_terms
from cranEval import CranEval
from matplotlib import pyplot as plt
from time import time
from pprint import pprint

#select your locals path
cranAll_path = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/cranAll/"
cranQry_path = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/cranQry.txt"
cranRel_path = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/cranqrel"

index = VectorialIndex(textProcessor=TextProcessor(unnused_characters=no_terms))



def index_time(index:Index, coleccion_path:str, rep:int = 5)->None:
    i = 0
    times:list[float] = []
    while i < rep:
        i+=1
        start = time()
        index.add_source(coleccion_path)
        end = time()
        print(f"start:{start}   end:{end}  time-{i}:{round(end-start,2)}")
        times.append((end-start))
        index.clean()
    print(f"Index time promedio: {round(sum(times)/rep,2)}")

def cran_metrics(index:Index, cranAll_path:str, cranQry_path:str, cranRel_path:str, save:bool=False):
    cranEval = CranEval(index=index, cranAll=cranAll_path, cranQry=cranQry_path, cranRel=cranRel_path)
    cranEval.retrieval_all_query()
    cranEval.compute_all_queries_metrics()

    p = cranEval.get_Metric('precision')
    r = cranEval.get_Metric('recall')
    f1 = cranEval.get_Metric('F1')
    fall = cranEval.get_Metric('fallout')

    for rank, vals in f1.items():
        fig, ax = plt.subplots()
        ax.set_ylabel('#queries')
        ax.set_xlabel('F1')
        fig.suptitle(f'F1 metric {rank}', fontsize=15)
        plt.hist(vals,color='darkcyan')
        plt.show()
        if save:
            fig.savefig(f'F1 metric {rank}.png')
        pprint(f"F1 promedio {rank}: {round(sum(vals)/len(vals),4)}")

    for rank, vals in p.items():
        fig, ax = plt.subplots()
        ax.set_ylabel('#queries')
        ax.set_xlabel('Precision')
        fig.suptitle(f'Presicion metric {rank}', fontsize=15)
        plt.hist(vals,color='mediumblue')
        plt.show()
        if save:
            fig.savefig(f'Presicion metric {rank}.png')
        pprint(f"Precision promedio {rank}: {round(sum(vals)/len(vals),4)}")

    for rank, vals in r.items():
        fig, ax = plt.subplots()
        ax.set_ylabel('#queries')
        ax.set_xlabel('Recall')
        fig.suptitle(f'Recall metric {rank}', fontsize=15)
        plt.hist(vals,color='indigo')
        plt.show()
        if save:
            fig.savefig(f'Recall metric {rank}.png')
        pprint(f"Recall promedio {rank}: {round(sum(vals)/len(vals),4)}")

    for rank, vals in fall.items():
        fig, ax = plt.subplots()
        ax.set_ylabel('#queries')
        ax.set_xlabel('Fallaout')
        fig.suptitle(f'Fallaout metric {rank}', fontsize=15)
        plt.hist(vals,color='darkmagenta')
        plt.show()
        if save:
            fig.savefig(f'Fallaout metric {rank}.png')
        pprint(f"Fallaout promedio {rank}: {round(sum(vals)/len(vals),4)}")

    for rank, vals in p.items():
        rec = r[rank]
        fig, ax = plt.subplots()
        ax.set_ylabel('recall')
        ax.set_xlabel('precision')
        fig.suptitle(f'Recall-Precision {rank}', fontsize=15)
        plt.scatter(vals, rec, s=44, color='cadetblue', alpha=0.6)
        plt.show()
        if save:
            fig.savefig(f'Recall-Precision {rank}.png')


index_time(index, cranAll_path)