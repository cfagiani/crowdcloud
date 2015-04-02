import requests, json

BASE_URL = "https://disqus.com/api/3.0/"
POSTS_API  = "posts/list.json"
THREADS_API = "threads/list.json"


class Disqusclient:
    """RESTful client for the Disqus API. This class depends on the 'requests' library.

    To instantiate the library, you must specify the api public key in the constructor
    """
    def __init__(self,apiKey):
        self.apiKey = apiKey
        self.threadDetails = {}


    def fetchPosts(self,forum, nextCursor=None, augmented=True):
        """Fetches a list of posts (100 at a time) and returns the data (as a list of dictionaries) and the cursor string for the "next" page

        If the augmented flag is passed in as True, then this class will augment the post data with information from the corresponding thread
        specifically the link and thread title. To minimize the number of api calls, the thread details are cached in memory so they are only fetched once.
        TODO: batch the requests to the threads api (it can take a series of "thread=" options
        """
        posts_url = BASE_URL + POSTS_API+"?forum="+forum+"&limit=100&api_key="+self.apiKey
        if(nextCursor != None):
            posts_url = posts_url+"&cursor="+nextCursor
        response = requests.get(posts_url)
        responseObj = json.loads(response.text)
        results = []
        for post in responseObj['response']:
            item = {'id':post['id'],
                    'msg':post['raw_message'],
                    'date':post['createdAt'],
                    'threadId':post['thread'],
                    'author':post['author'].get('username'),
                    'authorId':post['author'].get('id')}
            if(augmented):
                threadData = self.getThreadDetails(item['threadId'])
                item['link']=threadData['link']
                item['title']=threadData['title']
            results.append(item)
        nextCursor = None
        if(responseObj['cursor'] != None):
            nextCursor = responseObj['cursor'].get('next')
        return results, nextCursor

    def getThreadDetails(self, threadId):
        """Fetches the thread details from the api and caches them in memory
        
        """
        details =self.threadDetails.get(threadId)
        if(details is not None):
            return details
        else:
            response = requests.get(BASE_URL+THREADS_API+"?thread="+threadId+"&api_key="+self.apiKey)
            responseObj = json.loads(response.text)
            for thread in responseObj['response']:
                item = {'id':thread['id'],
                        'link':thread['link'],
                        'title':thread['clean_title']}
                self.threadDetails[threadId]=item
                return item
