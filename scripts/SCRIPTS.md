# SCRIPTS
This file will explain the assumptions these scripts have to be able to run,
along with how to change these scripts if you wish to run the scripts on a 
different collection of reddit posts.

Firstly, these scripts assume that ``api-results/`` and ``sentiment-results/``
already exist in the directory you clone the github repo into. 
That means there should be three directories before you run these scripts: 
``reddit-scraping/api-results/``, ``reddit-scraping/sentiment-results/``, 
and ``reddit-scraping/scripts/``.

## redditScrape.py
redditScrape.py already has a list of Reddit posts it gets information from, 
but if you want to run sentiment analysis on a different collection of posts, 
that is easily done.\
On line 20 of the script is a variable called ``url_list``, which contains a 
list of reddit post links that the script iterates through to get information 
from. You can edit this list with new links as you please. Be sure to put them 
in quotation marks ("\<link here\>") and put a comma after each new item. 

redditScrape.py assumes that there is a praw.ini file inside the ``scripts/`` 
directory that has information that lets the script access the Reddit API. 
It should look like this:
```
[bot1]
client_id=
client_secret=
user_agent=
password=
username=
```
You can find how to get this [information here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps). 
On the Beartooth cluster this information is already provided. Be sure NOT to 
share this info freely.  

## sentimentAnalyzer.py 
This script is responsible for going through the files created by "redditScrap.py" and  
organizing the information into an easy to read and and convenient format. In addition  
to this, it also collects data based on certain factors such as who commented the most,  
who replied the most, who replied to who, etc. Simply run the following command in order  
to run the script:
```  
python sentimentAnalyzer.py  
```
Please note that the user will have to download specific nltk libraries in order  
for this code to work. Once downloaded once, however, these libraries never have to  
be downloaded again. The required libraries are SentimentIntensityAnalyzer, word_tokenize,  
stopwords, and WordNetLemmatizer. By default, these will be downloaded to the home  
directory, although you can change the path to be whatever you want.  
These libraries are what allows for sentiment analysis of the comments and replies.
 
