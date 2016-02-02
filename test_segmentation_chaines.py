# encoding=utf8  

import normalisation,segmentation_chaines,structuration

def Main() :
    filename = "./donnees/Ecrits/tous_les_articles.txt"
    
    phrases = normalisation.Tokenize(filename)
    print "# : "+str(len(phrases))
    
    phrases1 = normalisation.Tokenize("./donnees/Ecrits/article_1.txt")
    phrases2 = normalisation.Tokenize("./donnees/Ecrits/article_2.txt")
    phrases3 = normalisation.Tokenize("./donnees/Ecrits/article_3.txt")
    phrases4 = normalisation.Tokenize("./donnees/Ecrits/article_4.txt")
    phrases5 = normalisation.Tokenize("./donnees/Ecrits/article_5.txt")
    #print phrases1
    print "1 : "+str(len(phrases1))
    print "2 : "+str(len(phrases1)+len(phrases2))
    print "3 : "+str(len(phrases1)+len(phrases2)+len(phrases3))
    print "4 : "+str(len(phrases1)+len(phrases2)+len(phrases3)+len(phrases4))
    print "5 : "+str(len(phrases1)+len(phrases2)+len(phrases3)+len(phrases4)+len(phrases5))
    tailleChaine = 200
    tailleFenetre = 8
    
    
    segments = segmentation_chaines.Segmentation(phrases, tailleChaine, tailleFenetre)
    
    print str(len(segments))+" segment(s) :"
    
    for segment in segments :
        print segment


if __name__ == '__main__' :
    Main()
    
    