import sys, argparse, dateutil.parser, json, string
from datetime import datetime


def main(args):
    """This program will output a word cloud as html based on the frequencies of words in a data file
    """
    
    with open(args.inputFile) as in_file:        
        data = json.load(in_file)
        counts = buildCounts(data,load_stopwords(args.stopFile))
        write_json(counts, args.outputFile,int(args.threshold))

def write_json(data,outputFile, threshold, asVariable=True):
    sortedData = sorted(data.items(),key=lambda x: x[1]['count'], reverse=True)
    with open(outputFile,'w') as out_file:
        count = 0
        if asVariable:
            out_file.write("var words = [")
        else:
            out_file.write("[")
        for item in sortedData:
            if(item[1]['count']<threshold):
               break
            if count > 0:
                out_file.write(",")
            count += 1
            out_file.write(json.dumps(item[1]))           
                        
        out_file.write("]")
        

        
                           

def load_stopwords(filename):
    words = set()
    with open(filename) as stop_file:
        for line in stop_file:
            words.add(line.strip())
    return words


def buildCounts(data, stop_words):
    words = {}
    for item in data:
        text = item['msg']
        for word in text.split():
            rawWord = sanitizeWord(word)
            word = rawWord.lower()
            if word not in stop_words and all(c in string.printable for c in word):
                record = words.get(word,None)
                if record == None:
                    record = {'count':1, 'word':rawWord,
                              'articles':{item['link']:item['title']}}
                    words[word]=record
                else:
                    record['count']=record['count']+1
                    record['articles'][item['link']]=item['title']
                    
    return words

def sanitizeWord(word):
    word = word.replace(".","").replace(",","").replace("?","").replace(":","").replace("(","").replace(")","").replace("*","").replace(";","").replace('"',"")
    return word
                
    
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Build a tag cloud from json data")
    argparser.add_argument("-i","--input", metavar='inputfile',required=True,help='file containing json data',dest='inputFile')
    argparser.add_argument("-o","--output", metavar='outputFile',required=True,help='output file',dest='outputFile')
    argparser.add_argument("-s","--stopfile", metavar="stopwordFile",default="stopwords.txt",help="stopwords file",dest="stopFile")
    argparser.add_argument("-t","--threshold", metavar="countThreshold",default=4,help="count threshold",dest="threshold")

    main(argparser.parse_args())
