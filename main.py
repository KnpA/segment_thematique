import glob,normalisation,segmentation,structuration

def Main():
    #Fichiers texte
    for textfile in glob.iglob('.\donnees\Ecrits\*.txt'):
        filename = textfile.split("\\")[3]
        print "Fichier "+filename
        

if __name__ == '__main__':
    normalisation.Test()
    segmentation.Test()
    structuration.Test()
    Main()