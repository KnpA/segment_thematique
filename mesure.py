# coding: utf8

def ecartSegments(reference, segments) :
    
    res = []
            
    tailleCum = 0
    for segment in segments :
        tailleCum += len(segment)
        res.append(tailleCum)
    
    reference2 = reference
    while len(reference2) < len(res) :
        reference2.append(0)

    while len(res) < len(reference2) :
        res.append(0)

    score = 0
    for i in range(0,len(res)) :
        score += abs(reference2[i] - res[i])
                
    return score