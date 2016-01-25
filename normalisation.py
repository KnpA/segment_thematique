# coding: utf8
import sys,glob,subprocess,shlex

reload(sys)  
sys.setdefaultencoding('utf-8')

def Test():
    #Lecture des textes et normalisation
    print "Normalisation des textes..."
    for textfile in glob.iglob('.\donnees\Ecrits\*.txt'):
        array = ReadTextFile(textfile)
    print "Normalisation OK"

def ReadTextFile(filepath):
    filepath = filepath.split("\\")
    filename = filepath[3]
    filepath = filepath[0]+"/"+filepath[1]+"/"+filepath[2]+"/"+filepath[3]
    print "Reading file "+filename
    return Tokenize(filepath)
        

def Tokenize(filename):
    #Tokenize
    args = shlex.split("perl normalization/tokenizer.pl --datafile normalization/tokenizer.data --language FRENCH "+filename)   
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    pipetext = p.communicate()[0]

    #Copy text to temp file
    f = open('tmp', 'w')
    f.write(pipetext)
    f.close()

    #Normalize
    args = shlex.split("perl normalization/normalizer.pl FRENCH tmp")   
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    pipetext = p.communicate()[0]

    #Convert to array
    sentences = pipetext.split("\n")
    array = []
    for sentence in sentences:
        words = sentence.split( )
        array.append(words)

    return array

if __name__ == '__main__':
    Test()