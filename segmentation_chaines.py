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
    
def Segmentation(phrases, tailleChaine, seuil) :
    
    chaines = CreerChaines(phrases, tailleChaine)
    
    print chaines
    
    segments = CreerSegments(phrases, chaines, seuil)
    
    print segments
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


def CreerSegments(phrases, chaines, seuil) :
    segments = []
    
    segment = []
    
    i = -1
    for phrase in phrases :
        i += len(phrase)
        
        segment += phrase
        
        print nbChaines(chaines, i)
        
        if (nbChaines(chaines, i) <= seuil) :
            
            print "segment"
            
            segments.append(segment)
            
            segment = []
    
    return segments

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