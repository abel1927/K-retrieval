
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