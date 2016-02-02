# encoding=utf8  
import normalisation,segmentation,structuration  

def Main():
    print "Main"

if __name__ == '__main__':
    normalisation.ReadXMLFiles()
    normalisation.Test()
    segmentation.Test()
    structuration.Test()
    Main()