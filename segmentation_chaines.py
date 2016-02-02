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

def Test():
    print "Segmentation chaines OK"
    
def Segmentation(phrases, tailleChaine, tailleFenetre) :
    
    chaines = CreerChaines(phrases, tailleChaine)
    
    #print chaines
    
    #segments = CreerSegments(phrases, chaines, seuil)
    
    sommeChaines = sumChaines(phrases, chaines)
    
    #print sommeChaines
    
    sommeChainesF = filtreGaussien5(sommeChaines)
    
    #print sommeChainesF
    
    frontieres = detecterSegments(sommeChainesF, tailleFenetre)
    
    #print frontieres
    
    segments =  CreerSegments(phrases,frontieres)
    
    #print segments
    return segments

def CreerChaines(phrases, tailleChaine) :
    
    chaines = {}
    compteurs = {}
    
    i = 0
    for phrase in phrases :
        for mot in phrase :
            
            
            # MAJ chaines
            if mot in compteurs.keys() :
                
                chaines[mot][-1].append(i)
                
            else :
                if mot not in chaines.keys() :
                    chaines[mot] = []
                    
                chaines[mot].append([i])
                
            
            # MAJ compteurs
            for cleCompteur in compteurs.keys() :
                
                if compteurs[cleCompteur] == 1 :
                    del compteurs[cleCompteur]
                else : 
                    compteurs[cleCompteur] = compteurs[cleCompteur]-1
                
            compteurs[mot] = tailleChaine
            
            i += 1;
            
            
    return chaines


def CreerSegments(phrases, frontieres) :
    segments = []
    
    segment = []
    frontiere = frontieres.pop(0)

    i = 0
    for phrase in phrases :
        #print phrase
        #print len(phrase)
        segment += phrase
        #print segment
        
        if i >= frontiere :
            
            #print "segment"
            
            
            segments.append(segment)
            
            segment = []
            
            if (len(frontieres) !=0 ) :
                frontiere = frontieres.pop(0)
        
        i += 1
    
    return segments

def sumChaines(phrases, chaines) :
    
    sumChaine = [];
    
    pos = -1
    for phrase in phrases :
        pos += len(phrase)
        sumChaine.append(nbChaines(chaines,pos))
        
    #print len(sumChaine)
    return sumChaine

def detecterSegments(sumChaine, tailleFenetre) :
    
    pos = tailleFenetre
    
    res = []
    
    while pos < len(sumChaine)-tailleFenetre :
        fenAvant = sumChaine[pos-tailleFenetre:pos]
        fenMilieu = sumChaine[pos]
        fenApres = sumChaine[pos+1:pos+1+tailleFenetre]
        
        if fenMilieu < min(fenAvant) and fenMilieu < min(fenApres) :
            #print "FRONTIERE"+str(pos)
            res.append(pos)
        pos += 1
        
    #print "FRONTIERE"+str(len(sumChaine)-1)
    res.append(len(sumChaine)-1)
   
    return res
    
def filtreGaussien5(tab) :
    
    pos = 2
    
    res = tab[0:2]
    
    while pos < len(tab)-2 :
        
        res.append((tab[pos-2]+2*tab[pos-1]+4*tab[pos]+2*tab[pos+1]+tab[pos])/10);
        
        pos = pos+1
        
    for elem in tab[pos:] :
        
        res.append(elem)
        
    
    return res
    

def nbChaines(chaines, position) :
    
    cpt = 0;
    
    for key in chaines.keys() :
        
        #print chaines[key]
        for chaine in chaines[key] :
            #print chaine
            if min(chaine) <= position and max(chaine) >= position :
                cpt += 1
        
        
    return cpt
            
            

def Main():
    #print stub
    Segmentation(stub, 4, 2)

if __name__ == '__main__':
    Main()