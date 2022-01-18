
def precision(rr:int, ir:int)->float:
    return rr/(rr+ir) if rr+ir > 0 else -1

def recovered(rr:int, rt:int)->float:
    return rr/rt if rt > 0 else -1

def F(rr:int, ir:int, rt:int, beta:float = 1)->float:
    p = precision(rr,ir)
    r = recovered(rr, rt)
    numertator = (1+(beta)**2)*p*r
    denominator = (beta**2)*p + r
    return numertator/denominator if denominator > 0 else -1

def fallaout(ri:int, it:int)->float:
    return ri/it if it > 0 else -1