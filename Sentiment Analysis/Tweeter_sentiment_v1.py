#Importing required libraries for sentiment analysis
from textblob import TextBlob
import tweepy
import json

Auth_file = open("auth_keys.json")
Auth_keys = json.load(Auth_file)

# print(Auth_keys["consumer_key"])

#Providing required keys for acessing data through tweeter 
auth=tweepy.OAuthHandler(Auth_keys["consumer_key"],Auth_keys["consumer_secret"])
auth.set_access_token(Auth_keys["access_token"],Auth_keys["access_token_secret"])
api=tweepy.API(auth)
#Collecting the tweets by giving company name

date_since="2020-03-01"
public_tweets= tweepy.Cursor(api.search,q='sbi',lang='en',since=date_since).items(500)
positive=0
negative=0
neutral=0
polr=0
#Classifying tweets as positive,neutral and negative using textblob library
for tweet in public_tweets:
    analysis=TextBlob(tweet.text)
    polr=polr+analysis.sentiment.polarity
    if analysis.sentiment.polarity>0:
        positive=positive+1
    elif analysis.sentiment.polarity<0:
        negative=negative+1
    else:
        neutral=neutral+1
#Results showing number of tweets of each category and overall polarity between(-1,1)
print('Positive',positive)
print('Negative',negative)
print('Neutral',neutral)
print('Polarity',polr/100)
