import tweepy
import os
import pandas as pd
import auth
import sys
from os import path
import csv


def headers_adder(file_name):
    with open(file_name,'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        headers = ["ID","Status","Created At","Text","Polarity"] 
        csv_writer.writerow(headers)
        print("Headers Written Successfully")


search_about = sys.argv
print(str(search_about[1]))

file_name = str(search_about[1])+'_tweets.csv'

File_Does_Not_Exist = not path.exists(file_name)


if File_Does_Not_Exist :
    headers_adder(file_name)
else:
    Empty_File_Check = True if path.getsize(file_name) == 0 else False
    if Empty_File_Check :
        headers_adder(file_name)


auth=tweepy.OAuthHandler(auth.consumer_key,auth.consumer_secret)
auth.set_access_token(auth.access_token,auth.access_token_secret)
api=tweepy.API(auth)

date_since="2020-03-01"

public_tweets = tweepy.Cursor(api.search,q=str(search_about[1]) ,lang='en',since=date_since,tweet_mode='extended').items(2);


# file_name = "tweets.csv"

file = pd.read_csv(file_name,index_col=0)

if file.empty:
    previous_lastest_tweet_ID = 0
else:
    previous_lastest_tweet_ID = file.head(1)["ID"]

# print(int(previous_lastest_tweet_ID))

for tweets in public_tweets:

    if int(previous_lastest_tweet_ID) == int(tweets.id) :
        print("Tweets all ready Exists")
        break

    if 'retweeted_status' in dir(tweets):
        text=tweets.retweeted_status.full_text
        status="retweet"
    else:
        text=tweets.full_text
        status="tweet"
    # count=count+1
    text = text.replace("\n"," ")
    row = pd.DataFrame({"ID":str(tweets.id) , "Status":status ,"Created At":str(tweets.created_at),"Text":text,"Polarity":0},index=[0])
    file = pd.concat([row,file]).reset_index(drop=True)

file["Created At"] = pd.to_datetime(file["Created At"])
file = file.sort_values(by="Created At",ascending=False)

file.to_csv(file_name)
print("File Written Successfully")