__author__ = 'Tarek Hoteit'
# This script first queries the list of companies' stock symbols in the database. It then picks up on an iterative
# basis a sample set of stock symbols to search for on Twitter in real-time streaming. Tweets associated with the
# stocks are then stored in the TwitterText database.
#To run the script:
#    runscript company_tweets_collect -v3 --settings=finSentiment.local_settings

import tweepy
from tweepy import StreamListener
from twitterSentiment import models
from datetime import datetime
from pytz import timezone
import json, time, sys
from numpy import random
import re
from django.contrib.auth.models import User
from twitterSentiment.models import Company
import pandas as pd
import schedule

import finSentiment.local_settings as settings

#initialize variables
companies = Company.objects.all()  # get the list of companies from the database
stocks = pd.DataFrame(list(companies.values('symbol')))  # get the stock symbols
stocks['symbol'] = stocks['symbol'].apply(lambda x: str('$'+x.strip()))

auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
auth.set_access_token(settings.access_token, settings.access_token_secret)
api = tweepy.API(auth)

systemid = User.objects.get(username="system").id



def timeupdate(twitterdate):
    # method to return a django-supported time from twitter-based time entry
    # input comes in the following fashion: Tue Jul 02 14:33:59 +0000 2013
    # return 2013-06-18 18:23:22-04:00
    central = timezone('US/Central')
    return central.localize(datetime.strptime(twitterdate, '%a %b %d %H:%M:%S +0000 %Y'))


class twitterListener(StreamListener):

    def __init__(self, api = None, fprefix = 'streamer'):
        self.api = api or tweepy.API()
        self.counter = 0
        self.time = time.time()
        return

    def on_data(self, data):
        global systemid
        self.counter += 1
        try:
            tweet = json.loads(data) #convert twitter stream in json into Python dictionary
            if isinstance(tweet, dict):
                if tweet['user']['lang'] != 'en': #only store english tweets
                    return
                else:
                    twitterDatabase(tweet)
                    print("tweets count: %d / %d, tweet: %s " % (self.counter, settings.tweets_max_per_sample, tweet['text']))
        except:
            print("Error in Twitter listener. Error message:", sys.exc_info())

        if self.counter > settings.tweets_max_per_sample:
            self.counter = 0
            return False
        else:
            return


    def on_limit(self, track):
        print(">> limit")
        return

    def on_error(self, status_code):
        print(">>> error: ", str(status_code) + "\n")
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False
        return

    def on_disconnect(self, notice):
        print (">> disconnecting")
        return False

    def on_timeout(self):
        print(">>> timed out ...\n")
        return False


def companyNamesbyStocks(tweet):
    #extract a list of company id for each stock symbol captured from the detected tweets
    #the data is then inserted in column TwitterText.twitter_text_keyword
    try:
        stockSymbolsinTweets = re.findall("\$\w+",tweet) #captures the stock symbols starting with $, such as $VZ
        stocksfound = ""
        for stock in stockSymbolsinTweets:
            try:
                astocksymboldfound = companies.get(symbol=str(stock).lstrip('$').upper())
                if astocksymboldfound:
                    stocksfound += ","+str(astocksymboldfound.id)
            except Company.DoesNotExist:
                pass
            except:
                print("Error in getting stock symbols from tweets:", sys.exc_info())
                pass;
        return stocksfound.lstrip(",")
    except:
        print("Error in getting stock symbols from tweets:", sys.exc_info())
        return "na"

def twitterDatabase(tweet):
    ## take Twitter financialdata in jsonformat and insert it into the database
    global systemid
    try:
        aTweet = models.TwitterText(twitter_userid=tweet['user']['id_str'],
                                    twitter_user_name=tweet['user']['screen_name'],
                                    twitter_text=tweet['text'],
                                    twitter_textid=tweet['id_str'],
                                    twitter_text_timestamp=timeupdate(tweet['created_at']),
                                    twitter_text_keyword=companyNamesbyStocks(tweet['text']),
                                    twitter_retweeted = tweet['retweeted'],
                                    training_user_id=systemid)
        aTweet.save()
    except:
        print("Error in Django insert tweet. error message:", sys.exc_info())
    return


def run_tweeter_listening():
    try:
        time.sleep(60)
        listener = twitterListener(api, "test")
        stream = tweepy.Stream(auth, listener)
        stocks_sample_df = stocks.sample(n=settings.tweets_polling_size).to_csv(header=False, line_terminator=',', index=False)
        print("Begin Twitter streaming for ", str(stocks_sample_df).rstrip(','))
        stream.filter(track=[stocks_sample_df], async=True)
    except:
        print(sys.exc_info())

def stop_tweeter_listening():
    print("stop")

def run():
    try:#schedule.every(settings.tweets_polling_time).seconds.do(stop_tweeter_listening)
        schedule.every(settings.tweets_polling_time).seconds.do(run_tweeter_listening)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        print(sys.exc_info())