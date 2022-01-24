
def precision(rr:int, ir:int)->float:
    return rr/(rr+ir)

def recall(rr:int, rt:int)->float:
    return rr/rt

def F(rr:int, ir:int, rt:int, beta:float = 1)->float:
    p = precision(rr,ir)
    r = recall(rr, rt)
    numertator = (1+(beta)**2)*p*r
    denominator = (beta**2)*p + r
    return numertator/denominator

def fallaout(ri:int, it:int)->float:
    return ri/it

def avg_precision(relevants:list[int], responses:list[int]):
    precisions = []
    rr = 0
    for i in range(len(responses)):
        if responses[i] in relevants:
            rr+=1
        precisions.append(rr/(i+1))
    return sum(precisions)/len(precisions)

def mean_avg_precision(avg_precision:float, total_queries:float)->float:
    pass