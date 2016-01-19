import sys,glob,subprocess,shlex

reload(sys)  
sys.setdefaultencoding('iso-8859-1')

def Test():
    #Fichiers texte
    ReadTextFiles()
    print "Normalisation OK"
        
def ReadTextFiles():
    for textfile in glob.iglob('.\donnees\Ecrits\*.txt'):
        filename = textfile.split("\\")
        filename = filename[0]+"/"+filename[1]+"/"+filename[2]+"/"+filename[3]
        print filename
        Tokenize(filename)

def Tokenize(filename):
    print "Tokenize "+filename
    args = shlex.split("perl ./normalization/tokenizer.pl --no-line-seg --datafile ./normalization/tokenizer.data --language FRENCH < "+filename)
    print args
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    pipetext = p.communicate()
    print str(pipetext[0])

if __name__ == '__main__':
    Test()