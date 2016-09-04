__author__ = 'Tarek Hoteit'
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

companies = Company.objects.all()  # get the list of companies from the database

stocks = pd.DataFrame(list(companies.values('symbol')))  # get the stock symbols
stocks['symbol'] = stocks['symbol'].apply(lambda x: str('$'+x.strip()))

tweetsmax = 500  #pick maximum 500 tweets for each company
tweetscount = 1
alltweetscount = 1
iterationcount = 1
systemid = "system"


def run_tweeter_listening():
    try:
        stocks_sample_df = stocks.sample(n=settings.tweets_polling_size).to_csv(header=False, line_terminator=',', index=False)
        twitterStreaming(stocks_sample_df)
    except:
        print(sys.exc_info())

def stop_tweeter_listening():
    print("stop")


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
        return

    def on_data(self, data):
        global tweetsmax
        global tweetscount
        global alltweetscount
        global iterationcount
        global systemid
        print("tweets count:",tweetscount, "/",tweetsmax,". Iteration: ",iterationcount," Total tweets: ", alltweetscount)
        if tweetsmax == tweetscount:
            tweetscount=0
            iterationcount += 1
            return False
        else:
            tweetscount += 1
            alltweetscount += 1
        try:
            tweet = json.loads(data) #convert twitter stream in json into Python dictionary
            print (tweet)
            if isinstance(tweet, dict):
                if tweet['user']['lang'] != 'en': #only store english tweets
                    return
                else:
                    print("tweet: ", tweet['text'])
                    twitterDatabase(tweet)
        except:
            print("Error in Twitter listener. Error message:", sys.exc_info())
        return

    def on_limit(self, track):
        print(">> limit")
        return

    def on_error(self, status_code):
        print(">>> error: ", str(status_code) + "\n")
        return

    def on_timeout(self):
        print(">>> timeout Sleeping for 60 seconds...\n")
        time.sleep(60)
        return

def companyNamesbyStocks(tweet):
    #extract the company behind each stock as the latter is mentioned in a tweet
    try:
        match = re.findall("\$\w+",tweet) #captures the stock symbols starting with $, such as $VZ
        global sp500_companies
        return ",".join(sp500_companies.Name.get(symbol,symbol)+"("+symbol+")" for symbol in match)
    except:
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


def twitterStreaming(stocks):
    try:
        print ("test"+settings.consumer_key)
        auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
        auth.set_access_token(settings.access_token, settings.access_token_secret)
        api = tweepy.API(auth)
        listener = twitterListener(api, "test")
        print ("Begin Twitter streaming for ", str(stocks).rstrip(','))
        stream = tweepy.Stream(auth, listener)
        stream.filter(track=[stocks])
    except:
        print ("Error in Twitter streaming",sys.exc_info())
    return True


def run():
    try:
        schedule.every(settings.tweets_polling_time).seconds.do(run_tweeter_listening)
        schedule.every(settings.tweets_polling_time).seconds.do(stop_tweeter_listening)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        print(sys.exc_info())