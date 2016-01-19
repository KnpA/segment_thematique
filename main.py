# encoding=utf8  
import sys, glob, subprocess, shlex  

reload(sys)  
sys.setdefaultencoding('utf8')

def Main():
    #Fichiers texte
    print "Reading files..."
    ReadTextFiles()

        
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
    Main()