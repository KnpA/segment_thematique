# coding: utf8
import sys,glob,subprocess,shlex
from lxml import etree

reload(sys)  
sys.setdefaultencoding('utf-8')

def ReadXMLFiles():
    for textfile in glob.iglob('./donnees/Transcriptions/ES/transcriptions/automatique/*.ssd'):
        filename = textfile#.split("\\");
        #filename = filename[1];
        print "________________________________________________________________________________";
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
                    print "passe"
            
            print("text : "+text)
    

def Test():
    #Fichiers texte
    ReadTextFiles()
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

if __name__ == '__main__':
    Test()