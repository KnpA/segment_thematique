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
    array = normalisation.ReadTextFile('./donnees/Ecrits/tous_les_articles.txt')
    print segmentation_tf.Segmentation(array)

if __name__ == '__main__':
    Main()
    