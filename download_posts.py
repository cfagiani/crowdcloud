"""
__author__ = 'Christopher Fagiani'

"""
from disqusclient import Disqusclient
import json
import sys, argparse, dateutil.parser
from datetime import datetime, timedelta


def main(args):
    """This program will download all the posts for a speific Disqus forum for a specific time interval (specified in hours on the command line)
    All data is written to a single output file as a well-formed JSON array.
    """
    gather_data(args.forum,args.interval,args.outputFile,args.key)

def gather_data(forum,interval, outputFile, apiKey):
    """Performs the actual work of downloading the data and writing the output file
    """
    stop_date = datetime.utcnow() - timedelta(hours=int(interval))
    with open(outputFile,'w') as out_file:        
        cursor = None
        last_date = None
        out_file.write("[")
        apiClient = Disqusclient(apiKey)
        posts, cursor = process_batch(apiClient,forum,None,stop_date)
        write_results(posts,out_file,True)
       
        while cursor is not None:
            posts, cursor = process_batch(apiClient,forum,cursor,stop_date)
            write_results(posts,out_file)
            
        out_file.write("]")
    


def write_results(data, out_file, first=False):
    """Writes the results to the file
    """
    for item in data:
        if(not first):
            out_file.write(",\n")
        else:
            first = False
        out_file.write(json.dumps(item))

def process_batch(apiClient, forum, cursor,stop_date):
    """Fetches a single batch of posts and checks the last date to see if we should stop processing
    this method returns the list of posts and the cursor string
    """
    last_date = None
    posts,cursor = apiClient.fetch_posts(forum,cursor,True)
    if(len(posts) > 0):
            last_date = dateutil.parser.parse(posts[-1]['date'])
    if(last_date == None or last_date < stop_date):
        cursor = None
    return posts,cursor


        
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Download all posts from a Disqus forum for a specific interval")
    argparser.add_argument("-i","--interval", metavar='intervalHours',default="24",help='interval in hours',dest='interval')
    argparser.add_argument("-f","--forum", metavar='forumName',required=True,help='forum name',dest='forum')
    argparser.add_argument("-k","--key", metavar='key',required=True,help='public key for api',dest='key')
    argparser.add_argument("-o","--output", metavar='outputFile',required=True,help='output file',dest='outputFile')

    main(argparser.parse_args())
