# coding: utf8
import sys,glob,subprocess,shlex
from lxml import etree

reload(sys)  
sys.setdefaultencoding('utf-8')

def ReadXMLFilesAuto():
    for textfile in glob.iglob('./donnees/Transcriptions/ES/transcriptions/automatique/*.ssd'):
        filename = textfile#.split("\\");
        #filename = filename[1];
        #print "________________________________________________________________________________";
        tree = etree.parse(filename)
        for ts in tree.xpath("/ssdoc/transcript/ts"):
            spk = ts.get("spk")
            start = ts.get("start")
            print ts.get("spk")
            text = "";
            for w in tree.xpath("/ssdoc/transcript/ts/w"):
                #print(" pop ")
                #w.getparent().get("spk")==spk and
                if ( w.getparent().get("start")==start):
                    text = text + w.get("str")+ " "
                    #print "passe"
            
            print(" "+text)
    

def Test():
    #Lecture des textes et normalisation
    print "Normalisation des textes..."
    for textfile in glob.iglob('./donnees/Ecrits/*.txt'):
        textfile = textfile.split("\\")
        filename = textfile[0]+'/'+textfile[1]
        array = Tokenize(filename)
        print array
    print "Normalisation OK"
        

def ReadTextFiles():
    for textfile in glob.iglob('.\donnees\Ecrits\*.txt'):
        filename = textfile.split("\\")
        filename = filename[0]+"/"+filename[1]+"/"+filename[2]+"/"+filename[3]
        #print "File: "+filename        
        text = Tokenize(filename)
        #print text

def Tokenize(filename):
    args = shlex.split("perl normalization/tokenizer.pl --no-line-seg --datafile normalization/tokenizer.data --language FRENCH "+filename)   
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    pipetext = p.communicate()[0]
    #print pipetext
    args = shlex.split("perl normalization/normalizer.pl --no-line-seg FRENCH "+filename)   
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    pipetext = p.communicate()[0]
    #print pipetext
    return pipetext

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
                if word.endswith('s'):
                    word = word[:-1]
                cleanSentence.append(word)
        cleanArray.append(cleanSentence)
    
    return cleanArray


def Tokenize(filename):
    #Tokenize
    args = shlex.split("perl normalization/tokenizer.pl --datafile normalization/tokenizer.data --language FRENCH "+filename)   
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    pipetext = p.communicate()[0]

    #Copy text to temp file
    f = open('tmp.txt', 'w')
    f.write(pipetext)
    f.close()

    #Normalize
    pipetext = Normalize('tmp.txt')

    #Convert in array
    array = TextToArray(pipetext)
    
    #Stop-Words
    cleanArray = StopList(array)

    return cleanArray

if __name__ == '__main__':
    Test()