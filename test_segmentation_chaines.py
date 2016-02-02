# encoding=utf8  

import normalisation,segmentation_chaines,structuration,mesure

def Main() :
    
    print "START"
    
    fichier = open("resultat_segmentation_chaine.txt","w")
    filename = "./donnees/Ecrits/tous_les_articles.txt"
    
    phrases = normalisation.Tokenize(filename)
    tailleCum = 0
    for phrase in phrases :
        tailleCum += len(phrase)
    fichier.write("texte * : "+str(tailleCum)+"\n")
    
    phrases1 = normalisation.Tokenize("./donnees/Ecrits/article_1.txt")
    phrases2 = normalisation.Tokenize("./donnees/Ecrits/article_2.txt")
    phrases3 = normalisation.Tokenize("./donnees/Ecrits/article_3.txt")
    phrases4 = normalisation.Tokenize("./donnees/Ecrits/article_4.txt")
    phrases5 = normalisation.Tokenize("./donnees/Ecrits/article_5.txt")
    #print phrases1
    
    reference = []
    
    tailleCum = 0
    for phrase in phrases1 :
        tailleCum += len(phrase)
    fichier.write("texte 1 : "+str(tailleCum)+"\n")
    reference.append(tailleCum)
    for phrase in phrases2 :
        tailleCum += len(phrase)
    fichier.write("texte 2 : "+str(tailleCum)+"\n")
    reference.append(tailleCum)
    for phrase in phrases3 :
        tailleCum += len(phrase)
    fichier.write("texte 3 : "+str(tailleCum)+"\n")
    reference.append(tailleCum)
    for phrase in phrases4 :
        tailleCum += len(phrase)
    fichier.write("texte 4 : "+str(tailleCum)+"\n")
    reference.append(tailleCum)
    for phrase in phrases5 :
        tailleCum += len(phrase)
    fichier.write("texte 5 : "+str(tailleCum)+"\n\n")
    reference.append(tailleCum)
    
    bestScore = float("inf")
    bestTailleChaine = 0
    bestTailleFenetre = 0
    
    for tailleChaine in range(50,301) :
        for tailleFenetre in range(1,101) :
    
            print "tailleChaine="+str(tailleChaine)+" - tailleFenetre="+str(tailleFenetre)
            fichier.write("### TRAITEMENT ###"+"\n\n")
            segments = segmentation_chaines.Segmentation(phrases, tailleChaine, tailleFenetre)
            fichier.write("tailleChaine="+str(tailleChaine)+" - tailleFenetre="+str(tailleFenetre)+"\n")
            fichier.write(str(len(segments))+" segment(s) :"+"\n")
            
            tailleCum = 0
            for segment in segments :
                tailleCum += len(segment)
                fichier.write("     "+str(tailleCum)+"\n")
            
            score = mesure.ecartSegments(reference, segments)
                
            fichier.write("  score="+str(score)+"\n")
            
            if (score < bestScore) :
                bestScore = score
                bestTailleChaine = tailleChaine
                bestTailleFenetre = tailleFenetre
            fichier.write(" --- "+"\n")
    
    
    fichier.write("  MEILLEUR SCORE="+str(bestScore))
    fichier.write("  MEILLEURE TAILLE CHAINE="+str(bestTailleChaine))
    fichier.write("  MEILLEURE TAILLE FENETRE="+str(bestTailleFenetre))
    fichier.write("END"+"\n")
    print "DONE"


if __name__ == '__main__' :
    Main()
    
    