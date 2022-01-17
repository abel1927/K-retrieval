from index import Index
from vectorialIndex import VectorialIndex
from text_processing import TextProcessor

def add_source(path:str, index:Index):
    index.add_source(path)

def retrieval(query:str, index:Index):
    rank = index.get_rank(query=query)
    return rank

no_terms = [' ', '.', ',', '!', '/', '(', ')', '?', ';', ':', 
        '...', "'", """""""", "”", "’", "“"]
index = VectorialIndex(textProcessor=TextProcessor(unnused_characters=no_terms))

source = "D:/AMS/Estudios/#3roS2/SRI/Proyecto Final/Test Collections/Test Collections/cran/cranAll/"
query = "what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft ."

add_source(source, index)

r = retrieval(query, index)

#i = True
for doc, s, text in r[0:30]:
    print(f"{doc} -- {round(s, 4)}")