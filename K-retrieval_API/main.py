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

add_source(source, index)

# from pprint import pprint

# pprint(index._all_words)
# print("\nDocumnets:")
# pprint(index._documents)
# print("\nDocumentsText")
# pprint(index._documentsText)
# print("\nDocumentsTokens")
# pprint(index._documentsTokens)
# print("\nWords Count")
# pprint(index._words_count)
# print("\nWords TF")
# pprint(index._words_TF)
# print("\nWords IDF")
# pprint(index._words_IDF)
# print("\nWords TFxIDF")
# pprint(index._words_TFxIDF)

while True:
    q = input("Query or e(for exit):")
    if q == "e":
        exit()
    r = retrieval(q, index)
    for doc, s in r[0:20]:
        print(f"{doc} -- {round(s, 4)}")
    print("----------------------------------------")