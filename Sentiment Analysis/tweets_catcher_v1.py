import csv
import tweepy
import json
import os
import pandas as pd

Auth_file = open("auth_keys.json")
Auth_keys = json.load(Auth_file)

auth=tweepy.OAuthHandler(Auth_keys["consumer_key"],Auth_keys["consumer_secret"])
auth.set_access_token(Auth_keys["access_token"],Auth_keys["access_token_secret"])
api=tweepy.API(auth)

date_since="2020-03-01"
public_tweets = tweepy.Cursor(api.search,q='sbi',lang='en',since=date_since,tweet_mode='extended').items(5);

fields = ["S.No","ID","Status","Created At","Text","polarity"]
file_name = "tweets.csv"

Empty_File_Check = True if os.path.getsize(file_name) == 0 else False

if(Empty_File_Check):
    with open(file_name,'a+') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(fields)
    print("Header Written Successfully")
else:
    print("File is Not Empty")
    # with open(file_name,'r') as csvfile:
    #     csv_reader = csv.reader(csvfile)
    #     for row in csv_reader:
    #         if

with open(file_name,'a+') as csvfile:
    count = 0
    csv_writer = csv.writer(csvfile)
    for tweets in public_tweets:
        if 'retweeted_status' in dir(tweets):
            text=tweets.retweeted_status.full_text
            status="retweet"
        else:
            text=tweets.full_text
            status="tweet"
        count=count+1
        text = text.replace("\n"," ")
        row = [count,tweets.id , status , str(tweets.created_at), text]
        csv_writer.writerow(row)

print("File Written Successfully")