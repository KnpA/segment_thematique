# coding: utf8
import math,tf_idf


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


def GlissementFenetre(vects,taille=3):
    ecarts={}
    maxi=-1
    for x in range(taille, len(vects)-taille+1):
        partie_gauche = {}
        partie_droite = {}
        for y in range(x-taille,x):
            partie_gauche=tf_idf.ConcatVecteur(partie_gauche,vects[y])
        for y in range(x,x+taille):
            partie_droite=tf_idf.ConcatVecteur(partie_droite,vects[y])
        ecarts[x]=tf_idf.Distance(partie_gauche,partie_droite)
        if ecarts[x] > maxi :
            maxi=ecarts[x]
    for k,v in ecarts.iteritems():
        ecarts[k] = v / float(maxi)
    return ecarts

def Test():
    print "Segmentation TF OK"
    
def Segmentation(phrases,threshold=0.5,fenetre=2,useTf=True,useIdf=True):
    segments = []    
    vects = []
    for phrase in phrases:
        vects.append(tf_idf.Phrase2Vecteur(phrase,useTf))
        #print Phrase2Vecteur(phrase)
    if useIdf:
        idf = tf_idf.InverseDocumentFrequency(vects)
        vects = tf_idf.AppliqueIDF(vects,idf)
    ecarts = GlissementFenetre(vects,fenetre)
    segment = []
    i = 0
    for phrase in phrases:
        if i in ecarts and ecarts[i] > threshold:
            segments.append(segment)
            segments.append("<br>")
            segment = []
        for mot in phrase:
            segment.append(mot)
        segment.append(". <b>END_P</b>")
        i += 1
    if segment != []:
        segments.append(segment)
    return segments

def Main():
    #print stub
    print Segmentation(stub)

if __name__ == '__main__':
    Main()