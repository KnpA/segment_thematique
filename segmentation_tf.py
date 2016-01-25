# coding: utf8
import math


stub = [
    ['a','b','a','c'],
    ['a','d','c','c'],
    ['b','d','e','e'],
    ['t','h','e','f'],
    ['t','h','k','f'],
    ['t','t','f','f'],
    ['t','t','f'],
    ['t','h','k','k','e'],
    ['r','t','j','k','e'],
]

def Phrase2Vecteur(phrase,normalize=True):
    """
    Convertit un phrase sous forme de vecteur en indiquant les occurences de chaque mot de la phrase
    """
    vect = {}
    for mot in phrase:  
        if mot in vect:
            vect[mot] += 1
        else:
            vect[mot] = 1
    #normalisation par rapport à la longueur de la phrase
    if normalize:
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
        for k,v in vect.iteritems():
            vect[k]=v*idf[k]
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

def GlissementFenetre(vects,taille=2):
    ecarts={}
    maxi=-1
    for x in range(taille, len(vects)-taille+1):
        partie_gauche = {}
        partie_droite = {}
        for y in range(x-taille,x):
            partie_gauche=ConcatVecteur(partie_gauche,vects[y])
        for y in range(x,x+taille):
            partie_droite=ConcatVecteur(partie_droite,vects[y])
        ecarts[x]=Distance(partie_gauche,partie_droite)
        if ecarts[x] > maxi :
            maxi=ecarts[x]
    for k,v in ecarts.iteritems():
        ecarts[k] = v / float(maxi)
    return ecarts

def Test():
    print "Segmentation TF OK"
    
def Segmentation(phrases):
    segments = []    
    vects = []
    for phrase in phrases:
        vects.append(Phrase2Vecteur(phrase))
        #print Phrase2Vecteur(phrase)
    idf = InverseDocumentFrequency(vects)
    vects = AppliqueIDF(vects,idf)
    ecarts = GlissementFenetre(vects)
    segment = []
    i = 0
    for phrase in phrases:
        if i in ecarts and ecarts[i] > 0.75:
            segments.append(segment)
            segment = []
        for mot in phrase:
            segment.append(mot)
        segment.append(".")
        i += 1
    if segment != []:
        segments.append(segment)
    return segments

def Main():
    #print stub
    print Segmentation(stub)

if __name__ == '__main__':
    Main()