# coding: utf8
import math,tf_idf

stub = [
    ['a','b','c','c'],
    ['a','b','c','c'],
    ['b','d','e','e'],
    ['t','h','e','f'],
    ['t','h','k','f'],
    ['t','t','f','f'],
    ['t','t','f'],
    ['t','h','k','k','e'],
    ['r','t','j','k','e'],
]


def Test():
    print "Structuration OK"

def ClassificationHierarchiqueAscendente(segments,nombre=5,useTf=False,useIdf=False):
    clusters = []
    inverseList = []
    idf = {}
    for segment in segments:
        clusters.append(segment)
        if useIdf:
            inverseList.append(tf_idf.Phrase2Vecteur(segment,useTf))
    if useIdf:
        idf = tf_idf.InverseDocumentFrequency(inverseList)
    while len(clusters) > nombre:
        vects = []
        candidate1 = -1
        candidate2 = -1
        minDistance = None
        for cluster in clusters:
            vects.append(tf_idf.Phrase2Vecteur(cluster,useTf))
            if useIdf:
                vects = tf_idf.AppliqueIDF(vects,idf)
        for i in range(0,len(clusters)):
            if candidate1 == -1:
                candidate1 = i
            for j in range(i+1,len(clusters)):                
                dist = tf_idf.Distance(vects[i],vects[j])
                print str(vects[i])+"__"+str(vects[j])
                print str(i)+" : "+str(j)+" - "+str(dist)
                if candidate2 == -1:
                    candidate2 = j
                    minDistance = dist
                else:
                    if dist < minDistance:
                        candidate1 = i
                        candidate2 = j
                        minDistance = dist
        #fuse canditate clusters
        print "Fusing ("+str(candidate1)+";"+str(candidate2)+") with dist = "+str(minDistance)
        #clusters[candidate1].append("<b>FUSE</b>")
        for mot in clusters[candidate2]:
                #print mot
                clusters[candidate1].append(mot)
        clusters.remove(clusters[candidate2])  
    return clusters

def Main():
    Test()
    print tf_idf.Distance({"a" : 1,"b" : 0},{"a" : 1,"b" : 0})
    print ClassificationHierarchiqueAscendente(stub,3,False,False)

if __name__ == '__main__':
    Main()