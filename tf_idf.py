# coding: utf8
import math


def Phrase2Vecteur(phrase,termFrequency=True,normalize=True):
    """
    Convertit un phrase sous forme de vecteur en indiquant les occurences de chaque mot de la phrase
    """
    vect = {}
    for mot in phrase: 
        if termFrequency and mot in vect:
            vect[mot] += 1
        else:
            vect[mot] = 1
    #normalisation par rapport à la longueur de la phrase
    if termFrequency and normalize:
        for k in vect:
            vect[k] = vect[k] / float(len(phrase))
    return vect

def InverseDocumentFrequency(vects):
    """
    Indique l'IDF de chaque mot dans la collection de vecteurs de phrase
    """
    idf = {}
    for vect in vects:
        for mot in vect:
            if mot in idf:
                idf[mot] += 1
            else:
                idf[mot] = 1
    for k,v in idf.iteritems():
        idf[k]=math.log(len(vects) / float(v))        
    return idf

def AppliqueIDF(vects,idf):
    """
    Applique l'IDF sur les vecteurs
    """    
    for vect in vects:
        if "<b>FUSE</b>" in vect:
            del vect["<b>FUSE</b>"]
        for k,v in vect.iteritems():
            if k in idf:
                vect[k]=v*idf[k]
            else:
                vect[k]=0
    return vects

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