CrowdCloud
==========

This project will build a simple word cloud based on the relative frequencies of words within the body of comments left on a Disqus forum.

Installation
-------------
* Install python 2.6+
* Install the Requests library: sudo pip install requests

If using the publisher as-is (i.e. with word lemmatization), follow these additional steps
* Install the Natural Language Toolkit: sudo pip install nltk
* Launch the python interpreter and run:
		import nltk
		nltk.download()
* Navigate to the Corpi page and select the WordNet corpus



Overview
----------

There are 3 main modules in the application that can be invoked independently:
* download_posts.py - this module is responsible for downloading the comment data from Disqus. 
* build_cloud.py - this module takes an output file containing comments in JSON format (i.e. the output of the download_posts module) and builds a new JSON structure that contains the word frequencies and their associated article links. 
* publisher.py - this module invokes the other two to download the data and transform it into a frequency dictionary. It then uploads the resultant data (the output of build_cloud) to a Dropbox folder using the Dropbox API.

TODO:
-----------
* clean up html by moving JS to another file
* make download_posts batch calls to the threads API 
* keep historic data and let users select day for which the cloud is displayed
