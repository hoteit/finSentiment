__author__ = 'tarek'
### the purpose of this file is to setup a training file that will be used to train Stanford CoreNLP Sentiment app
# the file will query the django finSentiment db twitterSentiment_twittertext table and generate a list of rows in
# format below
# {sentiment 0-4} {text}
# newline

import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import re, csv

dbconfig = {
	'database': 'finsentimentdb',
	'user': 'tarek',
	'password': 'TRhmyxpDobpi0gjt08Ja',
	'host': 'localhost',
	'raise_on_warnings': True,
	}

def stripnewlines(text):
	return re.sub(r"\n|\"",'',text)
	#return (text)


try:
	connectDB = mysql.connector.connect(**dbconfig)
	print("open connect")
	df = pd.read_sql("SELECT twitter_sentiment, twitter_text FROM `twitterSentiment_twittertext` where twitter_for_training=0", connectDB, columns=['sentiment','text'])
	df['train'] = df['twitter_sentiment'].map(str)+" "+df['twitter_text'].apply(stripnewlines)
	print(df['train'][72])
	## conver to text file
	df.to_csv("ready-to-train.txt",line_terminator="\n\n", columns=["train"], index=False, header=False,quotechar=' ')


except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exists")
	else:
		print(err)
else:
	print("conversion complete")
	connectDB.close()
