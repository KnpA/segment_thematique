# coding: utf8
import sys,glob,subprocess,shlex

reload(sys)  
sys.setdefaultencoding('utf-8')

def Test():
    #Fichiers texte
    ReadTextFiles()
    print "Normalisation OK"
        
def ReadTextFiles():
    for textfile in glob.iglob('.\donnees\Ecrits\*.txt'):
        filename = textfile.split("\\")
        filename = filename[0]+"/"+filename[1]+"/"+filename[2]+"/"+filename[3]
        text = Tokenize(filename)
        print "File: "+filename+"\n"+text

def Tokenize(filename):
    args = shlex.split("perl ./normalization/tokenizer.pl --no-line-seg --datafile ./normalization/tokenizer.data --language FRENCH "+filename)   
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    pipetext = p.communicate()[0]
    return pipetext

if __name__ == '__main__':
    Test()