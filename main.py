import glob

def Main():
    #Fichiers texte
    for textfile in glob.iglob('.\donnees\Ecrits\*.txt'):
        filename = textfile.split("\\")[3]
        print "Fichier "+filename

if __name__ == '__main__':
    Main()