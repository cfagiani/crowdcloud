"""
__author__ = 'Christopher Fagiani'

"""

import sys, argparse, dateutil.parser, json, string, collections
from datetime import datetime

SummaryData = collections.namedtuple('SummaryData', 'wordCounts articles commentCount authors anonCount') 

def main(args):
    """This program will output a word cloud as html based on the frequencies of words in a data file
    """
    process_data(args.threshold,args.inputFile,args.stopFile, args.outputFile)
    

def process_data(threshold,dataFile, stopwordsFile, outputFile, interval=None):
    with open(dataFile) as in_file:        
        data = json.load(in_file)
        summary_data = build_counts(data,load_stopwords(stopwordsFile))
        write_json(summary_data, outputFile,int(threshold),True,interval)
    


def write_json(summary_data, outputFile, threshold, asVariable=True, interval=None):
    """Writes a json file containing the count data for each word. If asVariable is true (the default), the data is output as a javascript variable declaration rather than a raw JSON array.
    """
    sortedData = sorted(summary_data.wordCounts.items(),key=lambda x: x[1]['count'], reverse=True)
    with open(outputFile,'w') as out_file:
        count = 0 
        if asVariable:
            out_file.write("var lastUpdated='"+datetime.now().strftime("%D at %H:%M:%S")+"';\n")
            out_file.write("var threshold='"+str(threshold)+"';\n")
            out_file.write("var commentCount='"+str(summary_data.commentCount)+"';\n")
            out_file.write("var articleCount='"+str(len(summary_data.articles))+"';\n")
            out_file.write("var authorCount='"+str(len(summary_data.authors))+"';\n")
            out_file.write("var anonCount='"+str(summary_data.anonCount)+"';\n")
            if interval is not None:
                out_file.write("var intervalHrs='"+interval+"';\n")
            else:
                out_file.write("var intervalHrs='unknown';\n")
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
    """loads the stopwords file
    """
    words = set()
    with open(filename) as stop_file:
        for line in stop_file:
            words.add(line.strip())
    return words


def build_counts(data, stop_words, lemmatize=True):
    """builds a dictionary keyed on the lowercase version of the sanizited string.
    The values are a dictionary that contains the raw word, the count of occurences
    and a dictionary of articles (keys = links, values = titles) for each article associated with the word.
    """
    words = {}
    commentCount = 0
    articles = set()
    authors = set()
    anonCount = 0
    lm = None
    if lemmatize:
        lm = initialize_lemmatizer()
    for item in data:
        commentCount += 1
        articles.add(item['link'])
        text = item['msg']
        authors.add(item['author'])
        if(item.get('authorId') == None):
            anonCount += 1
        for word in text.split():
            rawWord = sanitize_word(word)
            word = rawWord.lower()
            if lemmatize:
                word = lemmatize_word(lm,word)
            if word not in stop_words and all(c in string.printable for c in word):
                record = words.get(word,None)
                if record == None:
                    if rawWord == 'us':
                        print word
                    record = {'count':1, 'word':rawWord,
                              'articles':{item['link']:item['title']}}
                    words[word]=record
                else:
                    record['count']=record['count']+1
                    record['articles'][item['link']]=item['title']
                    
    return SummaryData(words, articles, commentCount, authors, anonCount)

def initialize_lemmatizer():
    """Initializes the wordnet lemmatizer. You must install nltk and download
    the wordnet corpus prior to using this method (after downloading nltk, import it and run nltk.download())
    """
    from nltk.stem.wordnet import WordNetLemmatizer
    return WordNetLemmatizer()

def lemmatize_word(lm,word):
    """Lemmatizes a word using the nltk library.
    Since we don't know the part of speech, this method performs 2 lemmatizations (once as a noun and once as a verb)
    The verson of the word that differs from the input word is returned.
    This is not always guaranteed to generate a correct answer, but it's good enough for our purposes.
    """                
    candidateN = lm.lemmatize(word,'n')
    candidateV = lm.lemmatize(word,'v')
    if candidateN == word:
        return candidateV
    else:
        return candidateN


def sanitize_word(word):
    """returns word after replacing common puctuation with the empty string
    """
    word = word.replace(".","").replace(",","").replace("?","").replace(":","").replace("(","").replace(")","").replace("*","").replace(";","").replace('"',"").replace("!","")
    word = word.replace("]","").replace("[","")
    return word
                
    
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Build a tag cloud from json data")
    argparser.add_argument("-i","--input", metavar='inputfile',required=True,help='file containing json data',dest='inputFile')
    argparser.add_argument("-o","--output", metavar='outputFile',required=True,help='output file',dest='outputFile')
    argparser.add_argument("-s","--stopfile", metavar="stopwordFile",default="stopwords.txt",help="stopwords file",dest="stopFile")
    argparser.add_argument("-t","--threshold", metavar="countThreshold",default=4,help="count threshold",dest="threshold")

    main(argparser.parse_args())
