# encoding=utf8  
import normalisation,segmentation_tf,segmentation_chaines,structuration,glob

def Main():
    print "Main"
    #normalisation.Test()
    segmentation_tf.Test()
    segmentation_chaines.Test()
    structuration.Test()    
    #Lecture des textes et normalisation
    print "Normalisation des textes..."
    array = normalisation.Tokenize('./donnees/Ecrits/tous_les_articles.txt')
    print segmentation_tf.Segmentation(array,threshold=0.925,fenetre=6,useTf=True,useIdf=True)

if __name__ == '__main__':
    normalisation.ReadXMLFilesAuto()
    normalisation.Test()
    #segmentation.Test()
    structuration.Test()
    Main()