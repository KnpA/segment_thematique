# coding: utf8
import sys,glob,subprocess,shlex,collections
from lxml import etree

reload(sys)  
sys.setdefaultencoding('utf-8')

# Fontion de test des lectures de fichiers et normalisation
def Test():
    #Lecture des textes et normalisation
    print "Normalisation des textes..."
    #ReadTextFiles()
    print "******************"
    print "Lecture des Références..."
    # Folder = ES, SaH ou INA
    #GetXMLReferences("ES")
    print "******************"
    print "Lecture des transcriptions auto..."
    # Folder = ES, SaH ou INA
    # Si Folder = INA alors subfolder = IRENE ou LIMSI
    #ReadXMLAutoFiles("SaH","LIMSI")
    print "******************"
    print "Ecriture des fichiers par topic"
    # Folder = ES, SaH ou INA
    # Si Folder = INA alors subfolder = IRENE ou LIMSI
    #WriteXMLAutoFilesWithRef("INA","IRENE")
    print "******************"
    print "Lecture des fichiers par topic"
    # Folder = ES, SaH ou INA
    # Si Folder = INA alors subfolder = IRENE ou LIMSI
    ReadTextAutoFiles("INA","IRENE")
    print "Normalisation OK"

# ********** Fichiers XML Référence **********
def GetXMLReferences(folder):
    for xmlfile in glob.iglob('./donnees/Reference/'+folder+'/*.ssd'):
        print "Fichier Référence: "+xmlfile
        GetXMLRef(xmlfile)

def GetXMLRef(xmlfile):
    ref = {}
    tree = etree.parse(xmlfile)
    for section in tree.xpath("/Trans/Section"):
        topic = section.get("topic")
        startTime = section.get("startTime")
        endTime = float(section.get("endTime"))
        ref[endTime] = topic
    return collections.OrderedDict(sorted(ref.items()))
    
# ********** Fichiers XML Auto **********

# Affichage du contenu des fichiers de transcription auto
def ReadXMLAutoFiles(folder, subfolder):
    if (folder == "INA"):
        subfolder = "/"+subfolder
    else:
        subfolder = ""

    for textfile in glob.iglob('./donnees/Transcriptions/'+folder+'/transcriptions/automatique'+subfolder+'/*.ssd'):
        ReadXMLAutoFile(textfile)

def ReadTextAutoFiles(folder, subfolder):
    if (folder == "INA"):
        if(subfolder == "LIMSI"):
            folder = "INA2"
    for textfile in glob.iglob('./donnees/Results/'+folder+'/*.ssd'):
        file = textfile.split("\\")
        file = file[0]+"/"+file[1]
        text = Tokenize(file)
        print text
      
def WriteXMLAutoFilesWithRef(folder, subfolder):
    if (folder == "INA"):
        subfolder = "/"+subfolder
    else:
        subfolder = ""
    
    # Pour chaque texte du dossier choisi
    for textfile in glob.iglob('./donnees/Transcriptions/'+folder+'/transcriptions/automatique'+subfolder+'/*.ssd'):        
        # On récupère le nom du fichier
        file = textfile.split("\\")
        file = file[1]
        print 'Fichier texte: '+file
        # On récupère le fichier de référence        
        with open('./donnees/Reference/'+folder+'/'+file) as refFile:
            # On récupère le tableau de startTime => topic
            ref = GetXMLRef(refFile)
            print ref
        # Pour chaque topic on crée un fichier vierge
        for d in ref.values():
            f = open('./donnees/Results/'+folder+'/'+file[:-4]+'_'+d+'.ssd', 'w')
            f.write("")
            f.close()
        # On crée un fichier par topic dans lequel on met les phrases associées
        tree = etree.parse(textfile)
        currentTopic = ""
        prev_spk = ""
        for ts in tree.xpath("/ssdoc/transcript/ts"):
            spk = ts.get("spk")
            start = ts.get("start")
            currentTopic = ""
            #print start
            for key, value in ref.iteritems():
                if float(start) < key:
                    currentTopic = value
                    break
            phrase = "";
            for w in ts:
                phrase = phrase + w.get("str")+" "
            if(spk != prev_spk):
                phrase = phrase[:-1]+".\n"
            prev_spk = spk
            f = open('./donnees/Results/'+folder+'/'+file[:-4]+'_'+currentTopic+'.ssd', 'a')
            f.write(phrase)
            f.close()    

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

# ********** Fichiers Texte **********

def ReadTextFiles():
    for textfile in glob.iglob('.\donnees\Ecrits\*.txt'):
        filename = textfile.split("\\")
        filename = filename[0]+"/"+filename[1]+"/"+filename[2]+"/"+filename[3]
        print "\nFichier: "+filename        
        text = Tokenize(filename)
        print text
      
# ********** Traitements **********

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