from index import Index
from text_processing import TextProcessor
from vectrorialIndex import VectorialIndex

def add_source(path:str, index:Index):
    index.add_source(path)

def retrieval(query:str, index:Index):
    rank = index.get_rank(query=query)
    return rank

no_terms = [' ', '.', ',', '!', '/', '(', ')', '?', ';', ':', 
        '...', "'", """""""", "”", "’", "“"]
index = VectorialIndex(textProcessor=TextProcessor(unnused_characters=no_terms))

source = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/cranAll/"

from time import time

s = time()
add_source(source, index)
e = time()

print(f"time: {round(e-s,4)}")

while True:
    q = input("Query or e(for exit):")
    if q == "e":
        exit()
    r = retrieval(q, index)
    for doc, s in r[0:20]:
        print(f"{doc} -- {round(s, 4)}")
    print("----------------------------------------")