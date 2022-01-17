
def vector_pow(vec:list[float])-> list[float]:
    return [x**2 for x in vec]

def vector_mult(vec_a:list[float], vec_b:list[float])->list[float]:
    if len(vec_a)!= len(vec_b):
        raise Exception("Vectors length incompatible")
    return [vec_a[i]*vec_b[i] for i in range(len(vec_a))]

def similarity(doc_vec:list[float], query_vec:list[float]) -> float:
    numerator = sum(vector_mult(doc_vec, query_vec))
    denominator = sum(vector_pow(doc_vec))**(1/2) * sum(vector_pow(query_vec))**(1/2)
    return numerator/denominator if denominator != 0 else 0