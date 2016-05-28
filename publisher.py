"""
__author__ = 'Christopher Fagiani'

"""
import requests, json, os, argparse
import download_posts, build_cloud


def main(args):
    """This program will use the download_posts and build_cloud modules to download all comment data and produce a
    tag cloud. It will then upload the resulting data to dropbox.
    """
    TEMP_DATA = "tempdata"
    TEMP_JSON = "cloud.json"
        
    download_posts.gather_data(args.forum, args.interval,TEMP_DATA,args.key)
    build_cloud.process_data(args.threshold,TEMP_DATA,args.stopFile,TEMP_JSON,args.interval)
    upload_file(TEMP_JSON, args.dropboxKey)
    cleanup_files([TEMP_DATA,TEMP_JSON])

def upload_file(fileName,token):
    """Uploads the file to the public dropbox folder
    """
    BASE_URL = "https://api-content.dropbox.com/1/files_put/auto/"
    with open(fileName) as in_file:
        data = in_file.read()
        headers = {"Authorization":"Bearer "+token}
        resp=requests.put(BASE_URL+"Public/"+fileName, data=data, headers=headers) 
        
def cleanup_files(fileNames):
    for f in fileNames:
        os.remove(f)       
    
        

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Builds data object that can be used to generate a word cloud from Disqus comments and uploads it to dropbox")
    argparser.add_argument("-i","--interval", metavar='intervalHours',default="24",help='interval in hours',dest='interval')
    argparser.add_argument("-f","--forum", metavar='forumName',required=True,help='forum name',dest='forum')
    argparser.add_argument("-dk","--disquskey", metavar='key',required=True,help='public key for disqus api',dest='key')
    argparser.add_argument("-dbk","--dbkey", metavar='dbkey',required=True,help='oauth token for drobpox api',dest='dropboxKey')
    argparser.add_argument("-s","--stopfile", metavar="stopwordFile",default="stopwords.txt",help="stopwords file",dest="stopFile")
    argparser.add_argument("-t","--threshold", metavar="countThreshold",default=10,help="count threshold",dest="threshold")
    main(argparser.parse_args())
