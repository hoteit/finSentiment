__author__ = 'Tarek Hoteit'
from twitterSentiment.models import Company
import pandas as pd
from finSentiment import settings
import sys
from django.utils import timezone
from scripts import utilities

# script that accesses the list of companies and stocks from
# NASDAQ website and imports them into the database and also creates a local file in directory.
# note: THIS WILL RECREATE THE COMPANY NAME RECORDS
#TODO: make the url configurable

nasdaqURL = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=%s&render=download'



def clean():
    # delete the records in the company table before importing the new companies
    try:
        Company.objects.all().delete() #delete all records in Company table
    except:
        print ("An error has occured: ", sys.exc_info())


def run():
    try:
        clean()  # clean existing files
        for exchange in ['amex', 'nyse', 'nasdaq']:
            companies = pd.read_csv(nasdaqURL % exchange, header=0)
            for idx, row in companies.iterrows():
                aCompany = Company(
                    symbol=row["Symbol"],
                    name=row["Name"],
                    ipoYear=row["IPOyear"],
                    lastSale=utilities.float_or_na(row["LastSale"]),
                    marketCap=utilities.millions(row["MarketCap"]),
                    sector=row["Sector"],
                    industry=row["industry"],
                    summaryQuote=row["Summary Quote"],
                    exchange=exchange,
                    date_extracted=timezone.now()
                )
                aCompany.save()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except:
        print("An error has occured: ",sys.exc_info())