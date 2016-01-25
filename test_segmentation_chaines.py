# encoding=utf8  

import normalisation,segmentation_chaines,structuration

def Main():
    filename = "./donees/Ecrits/tous_les_articles.txt"
    
    txt = normalisation.Tokenize(filename)
    
    print txt

if __name__ == '__main__':
    Main()
    
    