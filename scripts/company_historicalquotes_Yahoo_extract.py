__author__ = 'tarek'
import pandas as pd
import urllib
import time
import sys
from twitterSentiment.models import Company, CompanyQuoteHistory

#script that loops over every company  and then retrieve the start quote and end quote for the time of the tweets


def company_quote_history_data(company_id, stock, startDate, endDate):
    #function to query Yahoo YQL and return the financial financialdata for a stock based on stock symbol.
    #the variables are selected according to Altman Z-Score
    stock = stock.strip('$')
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    #extract financialdata from balance sheet
    yql_bs_query = "select * from yahoo.finance.historicaldata where symbol = '"+stock+"' and startDate= '"+startDate+"' and endDate = '"+endDate+"'"
    yql_bs_url = baseurl + urllib.parse.urlencode({'q':yql_bs_query}) + "&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
    as_json = pd.io.json.read_json(yql_bs_url)
    if as_json["query"]["results"] is not None:
       if as_json["query"]["results"]["quote"] is not None:
           for quote in as_json["query"]["results"]["quote"]:
               print(quote)
               if quote is not None:
                   try:
                       aCompanyQuote = CompanyQuoteHistory(company_id = company_id,
                                                        date = quote["Date"],
                                                        low = quote["Low"],
                                                        high = quote["High"],
                                                        close = quote["Close"],
                                                        open = quote["Open"],
                                                        volume = quote["Volume"],
                                                        adjs_close = quote["Adj_Close"],
                                                        symbol = quote["Symbol"])
                       aCompanyQuote.save()
                   except:
                       print ("error with stock:", stock, "error:",sys.exc_info())
               else:
                   print('done')
    return True


def run():
    get_companies = Company.objects.all()
    for company in get_companies:
        company_quote_history_data(company.id, company.symbol, '2016-09-01', '2016-09-05')