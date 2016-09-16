__author__ = 'tarek'


from twitterSentiment.models import Company, TwitterText, CompanySentiment
import subprocess
import re
import sys
import mysql.connector
from django.contrib.auth.models import User
from django.core import exceptions

corenlpcp = "/home/tarek/phd/nlp/stanford-corenlp-full-2014-10-31/*"
model = "/home/tarek/phd/nlp/stanford-corenlp-full-2014-10-31/model.ser.gz"

sentimentlevel = {'Very negative': 0,'Negative' :1, 'Neutral' : 2, 'Positive' : 3, 'Very positive' :4 }
sentimentregstr = re.compile(r"\s+(Positive|Negative|Neutral|Very negative|Very positive)\n\(.*?\n\s+0\:\s+(\w.*?)\s+(\w.*?)\s+(\w.*?)\s+(\w.*?)\s+(\w.*?)\n",re.DOTALL)
companykeywordreg = re.compile(r"\((.*?)\)", re.DOTALL)

def sentiments(text):
		# function that takes text, runs java corenlp and return output in string format
		text = subprocess.Popen(['echo', text], stdout=subprocess.PIPE,)
		sentiment = subprocess.Popen(['java','-cp',corenlpcp,'-mx5g',
																 'edu.stanford.nlp.sentiment.SentimentPipeline',
																 '-sentimentModel', model, '-stdin', '-output',
																 'ROOT,PROBABILITIES'], stdin=text.stdout,
																 stdout=subprocess.PIPE,)
		text.stdout.close()
		output = sentiment.communicate()[0]
		#sentiment.stdout.close()
		text.kill()
		return (output.decode("utf-8"))  # decode is necessary for the pattern match

def update_tweet(id, sentiment, user):
	# update tweet with overall sentiment
		try:
				atweet = TwitterText.objects.get(id=id)
				atweet.twitter_sentiment = sentiment
				atweet.training_user_id = user
				atweet.save()
				print("tweet", id, "updated.")
				return True
		except:
				print("errors occured", sys.exc_info())
				return False

def run():
		try:
			systemid = User.objects.get(username="system").id  # this account is used to update Twitter table
			tweets = TwitterText.objects.filter(twitter_for_training=2)  # get all tweets that are ready to be trained.
			tweets_count = tweets.count()
			if tweets_count > 0:
				for twt in range (0, tweets_count):

					#do sentiment analysis
					tweet = tweets[twt]
					tweet_text = str(tweet.twitter_text).encode()
					tweet_id = tweet.id
					print("tweet id: ", tweet_id, "tweet text:", tweet_text)
					sentiment = sentiments(tweet_text)
					sentimentreg = sentimentregstr.match(str(sentiment))
					if sentimentreg is not None:
						print ("sentiment: ", sentimentreg.group(1))
						print ("very negative: ", sentimentreg.group(2))
						print ("negative: ", sentimentreg.group(3))
						print ("neutral: ", sentimentreg.group(4))
						print ("positive: ", sentimentreg.group(5))
						print ("very positive: ", sentimentreg.group(6))
					else:
						print ("no pattern match")

					#pick the companies to store the sentiment
					tweet_companies_symbols = companykeywordreg.findall(tweet.twitter_text_keyword)
					if tweet_companies_symbols is not None:
						for company_symbol in tweet_companies_symbols:
							#get company
							print(company_symbol)
							try:
								company = Company.objects.get(symbol=company_symbol)
							except Company.DoesNotExist:
								company = None

							if company is not None:
								companysentiment = CompanySentiment(company_id=company.id,twitter_text_id=tweet_id,
																	sentiment_root_value=sentimentreg.group(1),
																	sentiment_prob_very_negative=sentimentreg.group(2),
																	sentiment_prob_negative=sentimentreg.group(3),
																	sentiment_prob_neutral=sentimentreg.group(4),
																	sentiment_prob_positive=sentimentreg.group(5),
																	sentiment_prob_very_positive=sentimentreg.group(6))
								companysentiment.save()
								print("added tweet sentiment for company:",company_symbol)
							else:
								print("symbol ",company_symbol," does not exist in the database")
					update_tweet(tweet_id,sentimentlevel[sentimentreg.group(1)],systemid)
				TwitterText.objects.filter(twitter_for_training="2").update(twitter_for_training="4") #flag tweets as classified
			else:
				print ("no tweets remmaining to be classified for sentiments")
		except mysql.connector.Error as err:
			print("MySQL error: ", err.msg)
		except:
			print("error occured", sys.exc_info())


