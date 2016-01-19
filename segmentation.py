# coding: utf8
import math


stub = [
    ['a','b','a','c'],
    ['a','d','c','c'],
    ['b','d','e','e']
]

def Phrase2Vecteur(phrase):
    """
    Convertit un phrase sous forme de vecteur en indiquant les occurences de chaque mot de la phrase
    """
    vect = {}
    for mot in phrase:  
        if mot in vect:
            vect[mot] += 1
        else:
            vect[mot] = 1 
    return vect

def ConcatVecteur(vec1,vec2):
    """
    Concatène deux vecteurs
    """
    vect = {}
    for k,v in vec1.iteritems():
        vect[k]=v
    for k,v in vec2.iteritems():
        if k in vec1:
            vect[k]+=v
        else:
            vect[k]=v
    return vect

def Distance(vec1,vec2,L=2):
    """
    Calcule la distance-L entre deux vecteurs vec1 et vec2
    """
    dist = 0
    ref = ConcatVecteur(vec1,vec2)
    for k in ref:
        val1 = 0
        val2 = 0
        if k in vec1:
            val1 = vec1[k]
        if k in vec2:
            val2 = vec2[k]
        dist += math.pow(abs(val1 - val2),L)
    dist = math.pow(dist,1/float(L))
    return dist

def Test():
    print "Segmentation OK"

def Main():
    print stub
    vects = []
    for phrase in stub:
        vects.append(Phrase2Vecteur(phrase))
        print Phrase2Vecteur(phrase)
    print Distance(vects[0],vects[1])
    
    

if __name__ == '__main__':
    Main()