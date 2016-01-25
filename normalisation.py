# coding: utf8
import sys,glob,subprocess,shlex

reload(sys)  
sys.setdefaultencoding('utf-8')

def Test():
    #Lecture des textes et normalisation
    print "Normalisation des textes..."
    for textfile in glob.iglob('./donnees/Ecrits/*.txt'):
        textfile = textfile.split("\\")
        filename = textfile[0]+'/'+textfile[1]
        array = Tokenize(filename)
        print array
    print "Normalisation OK"
        
def Normalize(filename):
    #Normalize
    args = shlex.split("perl normalization/normalizer.pl FRENCH "+filename)   
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    pipetext = p.communicate()[0]
    return pipetext

def TextToArray(text):
    #Convert to array
    sentences = text.split("\n")
    array = []
    for sentence in sentences:
        words = sentence.split( )
        validwords = []
        for word in words:
            if len(word) > 1:
                word = word.lower()
                validwords.append(word)
        array.append(validwords)
    return array

def StopList(array):
    #Remove useless words
    cleanArray = []
    with open('./normalization/stopwords.txt') as f:
        stopList = [x.strip('\n') for x in f.readlines()]
    
    for sentence in array:
        cleanSentence = []
        for word in sentence:
            if word not in stopList:
                cleanSentence.append(word)
        cleanArray.append(cleanSentence)
    
    return cleanArray


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
    pipetext = Normalize('tmp')

    #Convert in array
    array = TextToArray(pipetext)
    
    #Stop-Words
    cleanArray = StopList(array)

    return cleanArray

if __name__ == '__main__':
    Test()