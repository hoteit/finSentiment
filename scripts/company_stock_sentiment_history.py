__author__ = 'tarek'

import pandas as pd
from django.db.models import Q
##load the django model
from twitterSentiment.models import Company, CompanyFinancials, TwitterText, CompanySentiment, CompanyQuoteHistory,CompanyStocksSentimentHistory
from datetime import date, timedelta
from time import strftime

def company_quote_calculations(companyid, adate):
    try:
        company_stock = CompanyQuoteHistory.objects.filter(company_id=companyid, date=adate)
        if company_stock.count() >0:
            company_stock_values = company_stock.values()
            stockopen = company_stock_values[0]['open']
            stockclose = company_stock_values[0]['close']
            if stockopen > stockclose:
                direction = -1
            elif stockopen < stockclose:
                direction = 1
            else:
                direction = 0
            return (stockopen, stockclose,direction)
        else:
            return (None, None, None)
    except:
        print ("quote error occured for company:", companyid, "error:",sys.exc_info())
        return (None, None, None)


def company_sentiment_calculations(companyid, date):
    try:
        company_sentiments = CompanySentiment.objects.filter(company_id=companyid,twitter_text__twitter_text_timestamp__startswith=date).values()
        if company_sentiments.count() >0:
            company_sentiments_list = pd.DataFrame(list(company_sentiments))
            averages = pd.Series([company_sentiments_list['sentiment_prob_very_negative'].astype(float).sum(),
                company_sentiments_list['sentiment_prob_negative'].astype(float).sum(),
                company_sentiments_list['sentiment_prob_neutral'].astype(float).sum(),
                company_sentiments_list['sentiment_prob_positive'].astype(float).sum(),
                company_sentiments_list['sentiment_prob_very_positive'].astype(float).sum()],
                index=[0,1,2,3,4])
            return (averages.idxmax(axis=1), company_sentiments.count()) #pick the index with the maximum probability
        else:
            return (None,None)
    except:
        print ("sentiment error occured for company:", companyid, "error:",sys.exc_info())
        return (None,None)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def run():
    start_date = date(2014, 12, 6)
    end_date = date(2015, 1, 5)
    companies = Company.objects.filter(~Q(marketCap=0.0))
    row = 0
   # df = pd.DataFrame(columns=('Date', 'Company', 'Symbol', 'Sentiment', 'Stock Open', 'Stock Close', 'Direction'))
    for company in companies:
        for single_date in daterange(start_date, end_date):
            querydate = strftime("%Y-%m-%d", single_date.timetuple())
            sentiment,tweet_count = company_sentiment_calculations(company.id,querydate)
            stock_open,stock_close,stock_direction  = company_quote_calculations(company.id,querydate)
            aCompanyStocksSentimentHistory = CompanyStocksSentimentHistory(company_id=company.id,
                                                                           symbol=company.symbol,
                                                                           date=querydate,
                                                                           tweet_count=tweet_count,
                                                                           sentiment = sentiment,
                                                                           stockopen = stock_open,
                                                                           stockclose = stock_close,
                                                                           stockdirection = stock_direction
                                                                           )
            aCompanyStocksSentimentHistory.save()
    #        df.loc[row]= [querydate, company.id, company.symbol, sentiment, stock_open, stock_close, stock_direction]
     #       print (df.loc[row])
            print (row,":company",company.symbol," date,", querydate," complete.")
            row = row +1

tweets = CompanySentiment.objects.filter(company_id=5207,twitter_text__twitter_text_timestamp__startswith = "2014-12-06")
tweets.count()
print (company_quote_calculations(5207, "2014-12-09"))