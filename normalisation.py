# coding: utf8
import sys,glob,subprocess,shlex
from lxml import etree

reload(sys)  
sys.setdefaultencoding('utf-8')

# Fontion de test des lectures de fichiers et normalisation
def Test():
    #Lecture des textes et normalisation
    print "Normalisation des textes..."
    #ReadTextFiles()
    print "******************"
    print "Normalisation des transcriptions auto..."
    # Folder = ES, SaH ou INA
    # Si Folder = INA alors subfolder = IRENE ou LIMSI
    ReadXMLAutoFiles("INA","LIMSI")
    print "Normalisation OK"
    
# Affichage du contenu des fichiers de transcription auto
def ReadXMLAutoFiles(folder, subfolder):
    if (folder == "INA"):
        subfolder = "/"+subfolder
    else:
        subfolder = ""

    for textfile in glob.iglob('./donnees/Transcriptions/'+folder+'/transcriptions/automatique'+subfolder+'/*.ssd'):
        ReadXMLAutoFile(textfile)

# Affichage du contenu d'un fichier de transcription auto
def ReadXMLAutoFile(filename):
    print "\nFichier: "+filename
    tree = etree.parse(filename)
    for ts in tree.xpath("/ssdoc/transcript/ts"):
        spk = ts.get("spk")
        start = ts.get("start")
        print "speaker="+ts.get("spk")+" start="+start
        phrase = "";
        for w in tree.xpath("/ssdoc/transcript/ts/w"):
            if ( w.getparent().get("start")==start):
                phrase = phrase + w.get("str")+" "
        print(phrase+"\n")
        

def ReadTextFiles():
    for textfile in glob.iglob('.\donnees\Ecrits\*.txt'):
        filename = textfile.split("\\")
        filename = filename[0]+"/"+filename[1]+"/"+filename[2]+"/"+filename[3]
        print "\nFichier: "+filename        
        text = Tokenize(filename)
        print text

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
        if(cleanSentence):
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