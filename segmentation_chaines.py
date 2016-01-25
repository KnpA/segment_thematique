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
    
def Segmentation(phrases, tailleChaine) :
    segments = []
    
    chaines = CreerChaines(phrases, tailleChaine)
     
    return segments

def CreerChaines(phrases, tailleChaine) :
    
    chaines = {}
    compteurs = {}
    
    i = 0
    for phrase in phrases :
        for mot in phrase :
            
            
            # MAJ chaines
            if mot in compteurs.keys() :
                print chaines[mot]
                chaines[mot]
                
            else :
                if mot not in chaines.keys() :
                    chaines[mot] = []
                    
                chaines[mot].append([])
            
            # MAJ compteurs
            for cleCompteur in compteurs.keys() :
                
                if compteurs[cleCompteur] == 1 :
                    del compteurs[cleCompteur]
                else : 
                    compteurs[cleCompteur] = compteurs[cleCompteur]-1
                
            compteurs[mot] = tailleChaine
            print compteurs
            
            i += 1;
            
            
    return chaines


def CreerSegments(chaines, tailleChaine) :
    segments = []
    
    return segments
            
            

def Main():
    #print stub
    Segmentation(stub, 3)

if __name__ == '__main__':
    Main()