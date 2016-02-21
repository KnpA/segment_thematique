# encoding=utf8  
import normalisation,segmentation_fenetre,segmentation_chaines,structuration,glob

def Main():
    print "Main"
    #normalisation.Test()
    segmentation_fenetre.Test()
    segmentation_chaines.Test()
    structuration.Test()    
    #Lecture des textes et normalisation
    print "Normalisation des textes..."
    array = normalisation.Tokenize('./donnees/Ecrits/tous_les_articles.txt')
    """
    resultats : TF = True & IDF = false
     --- 
    MEILLEUR SCORE=3059  MEILLEUR THRESHOLD=0.85  MEILLEURE TAILLE FENETRE=3END
    
    _____
    resultats : TF = True & IDF = True
    --- 
    MEILLEUR SCORE=3853  MEILLEUR THRESHOLD=0.9  MEILLEURE TAILLE FENETRE=1END
    """
    segments =  segmentation_fenetre.Segmentation(array,threshold=0.825,fenetre=3,useTf=True,useIdf=False)
    print segments
    for segment in segments:
        print segment
        print "<br />"
    print "Segmentation des textes OK"
    clusters = structuration.ClassificationHierarchiqueAscendente(segments,5,useTf=False,useIdf=True)
    for cluster in clusters:
        print cluster
        print "<br />"
    print "Clusterisation des textes OK"

if __name__ == '__main__':
    #normalisation.ReadXMLFilesAuto()
    normalisation.Test()
    #segmentation.Test()
    structuration.Test()
    Main()
