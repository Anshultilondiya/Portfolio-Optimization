<<<<<<< HEAD
import tweepy
import pandas as pd
import sys
from os import path
import csv
from textblob import TextBlob


# api = authentication.api

def headers_adder(file_name):
    print("Writing Headers")
    with open(file_name,'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        headers = ["ID","Status","Created At","Text","Polarity"] 
        csv_writer.writerow(headers)
        print("Headers Written Successfully")

def authentication():
    import auth
    auth=tweepy.OAuthHandler(auth.consumer_key,auth.consumer_secret)
    auth.set_access_token(auth.access_token,auth.access_token_secret)
    api=tweepy.API(auth)
    return api


def print_output(output):
    output = output.set_index("S.No.")
    print()
    x = range(50)
    for i in x:
        print("*",end=" ")
    print()
    print()
    print("Output of the Sentiment Analysis")
    print()
    print(output)
    print()
    for i in x :
        print("*",end=" ")
    print()
    print()
    



# search_about = sys.argv
# print(str(search_about[1]))

# file_name = str(search_about[1])+'_tweets.csv'

def sentiment_analysis(Companies_Names_Array):

    api = authentication()

    output_array =[]

    date_since="2020-03-01"
    
    print("Searching Latest Tweets For :")
    index = 0
    for company in Companies_Names_Array:
        index = index +1
        print("---------- "+ company + " ----------")

        file_name = company+'_tweets.csv'

        File_Does_Not_Exist = not path.exists(file_name)

        if File_Does_Not_Exist :
            print("Tweets File For "+company+" Does not Exist Already")
            print("Creating Tweet File For "+ company +" named : " +file_name)
            headers_adder(file_name)
        else:
            Empty_File_Check = True if path.getsize(file_name) == 0 else False
            if Empty_File_Check :
                print("Tweet File of "+company+" Found Empty")
                headers_adder(file_name)

        tweets_to_be_retrieve = 200

        public_tweets = tweepy.Cursor(api.search,q=str(company) ,lang='en',since=date_since,tweet_mode='extended').items(tweets_to_be_retrieve);

        file = pd.read_csv(file_name,index_col=0)

        if file.empty:
            previous_lastest_tweet_ID = 0
        else:
            previous_lastest_tweet_ID = file.head(1)["ID"]

        count = 0

        helper_text=""
        second_helper_text="All Other "


        for tweets in public_tweets:

            if int(previous_lastest_tweet_ID) == int(tweets.id) :
                if(count == 0):
                    second_helper_text=""
                print(second_helper_text+"Latest Tweets Already Exist in "+ file_name)
                helper_text="Only "
                break
            
            count = count+1

            if 'retweeted_status' in dir(tweets):
                text=tweets.retweeted_status.full_text
                status="retweet"
            else:
                text=tweets.full_text
                status="tweet"

            text = text.replace("\n"," ")

            analysis=TextBlob(text)
            polarity_strength = analysis.sentiment.polarity
            if polarity_strength>0:
                polarity = 1
            elif polarity_strength<0:
                polarity = -1
            elif polarity_strength == 0:
                polarity = 0

            row = pd.DataFrame({"ID":str(tweets.id) , "Status":status ,"Created At":str(tweets.created_at),"Text":text,"Polarity":polarity,"Polarity Strength":polarity_strength},index=[0])
            file = pd.concat([row,file]).reset_index(drop=True)

        file["Created At"] = pd.to_datetime(file["Created At"])
        file = file.sort_values(by="Created At",ascending=False)

        recent_tweets = file.head(200)

        recent_tweets_list = recent_tweets.values.tolist()

        positive_count=0
        negative_count=0
        neutral_count=0
        strength = 0
        for row in recent_tweets_list:
            polarity = row[4]
            strength  = strength + row[5]
            if(polarity == 1):
                positive_count = positive_count + 1
            elif(polarity == -1):
                negative_count = negative_count + 1
            elif(polarity == 0):
                neutral_count = neutral_count + 1
            results={"S.No.":index,"Name":company,"Positive Tweets": positive_count,"Negative Tweets":negative_count,"Neutral Tweets": neutral_count,"Polarity":strength/100}
        output_array.append(results)
        output  = pd.DataFrame(output_array)

        if(count !=0):
            print("Adding "+ helper_text +str(count)+" New Tweets to "+file_name)
            file.to_csv(file_name)
            print("File Written Successfully")

    print_output(output)
=======
import tweets_catcher
import textblob as TB 
>>>>>>> b0f8d2c9cb69ff391d120ee6ab0842ecc51f06e7
