__author__ = 'Tarek Hoteit'

import pandas as pd
import urllib
import sys
from django.utils import timezone
from twitterSentiment.models import Company, CompanyFinancials, CompanyAltmanZscore
from scripts import utilities

#script that reads each stock symbol in twitterSentiment_company table, gets the latest
#financials from MorningStar.com and Yahoo Finance, calculates Altman Z-Score and imports the records in twitterSentiment_companyfinancials


def altman_zscore(working_capital, total_assets,
                  total_liability, retained_earnings, ebitda, market_capital,sales):
    return ((1.2*working_capital / total_assets) + (1.4*retained_earnings / total_assets) +
            (3.3*ebitda / total_assets) + (0.6*market_capital / total_liability) + (0.999*sales / total_assets))


def financial_data(company_id, company_stock_symbol, accounting_year, quarter):
    #MorningStar URL are extracted from https://gist.github.com/hahnicity/45323026693cdde6a116

    ms_income_statement = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="+company_stock_symbol+\
                          "&reportType=is&period=3&dataType=A&order=desc&columnYear=5&number=3"
    ms_balance_sheet = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="+company_stock_symbol+\
                          "&reportType=bs&period=3&dataType=A&order=desc&columnYear=5&number=3"
    #ms_cash_flow = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="+company_stock_symbol+\
    #                     "&reportType=cf&period=3&dataType=A&order=desc&columnYear=5&number=3"

    #notes from hahnicity:   reportType: is = Income Statement, cf = Cash Flow, bs = Balance Sheet;
    #period: 12 for annual reporting, 3 for quarterly reporting
    #dataType: this doesn't seem to change and is always A
    #order: asc or desc (ascending or descending)
    #columnYear: 5 or 10 are the only two values supported
    #number: The units of the response data. 1 = None 2 = Thousands 3 = Millions 4 = Billions

    # TODO: ADD the publication and permission to use the data.

    total_assets=""
    total_liability=""
    current_assets=""
    current_liability=""
    retained_earnings=""
    market_capital = ""
    ebitda=""
    sales=""
    stockprice=""

    try:
        #read balance sheet
        balance_sheet = pd.read_csv(ms_balance_sheet, header=1, skiprows=0, index_col=0)
        total_assets=balance_sheet.loc['Total assets'][0]
        total_liability=balance_sheet.loc['Total liabilities'][0]
        current_assets=balance_sheet.loc['Total current assets'][0]
        current_liability=balance_sheet.loc['Total current liabilities'][0]
        retained_earnings=balance_sheet.loc['Retained earnings'][0]

        #read income statement
        income_statement = pd.read_csv(ms_income_statement, header=1, skiprows=0, index_col=0)
        ebitda = income_statement.loc['EBITDA'][0]
        sales = income_statement.loc['Revenue'][0]

        #extract latest stock info and market capital using Yahoo financialdata from finance quotes
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_qt_query = "select * from yahoo.finance.quotes where symbol in ('"+company_stock_symbol+"')"
        yql_qt_url = baseurl + urllib.parse.urlencode({'q':yql_qt_query}) + "&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
        qt_json = pd.io.json.read_json(yql_qt_url)
        try:
            stockprice = qt_json["query"]["results"]["quote"]["LastTradePriceOnly"]
        except:
            stockprice = "0"
        try:
            market_capital = utilities.millions(qt_json["query"]["results"]["quote"]['MarketCapitalization'])
        except:
            market_capital = "0"

        print(company_id,total_assets,total_liability,
            current_assets,current_liability,retained_earnings,
            market_capital,ebitda,sales,stockprice)

        companyFinancials = CompanyFinancials(company_id=company_id,
                                      total_assets=total_assets,
                                      total_liability=total_liability,
                                      current_assets=current_assets,
                                      current_liability=current_liability,
                                      retained_earnings = retained_earnings,
                                      market_capital=market_capital,
                                      ebitda = ebitda,
                                      sales = sales,
                                      stockprice=stockprice,
                                      date_extracted=timezone.now(),
                                      year=accounting_year,
                                      quarter=quarter,)
        companyFinancials.save()
        companyFinancialsId = companyFinancials.id
        if companyFinancialsId is not None:
            altmanzscore = altman_zscore(current_assets-current_liability, total_assets,
                                     total_liability, retained_earnings, ebitda, market_capital, sales)
            companyAltmanZScore = CompanyAltmanZscore(
                company_id=company_id,
                company_financials_id=companyFinancialsId,
                zscore=altmanzscore)
            companyAltmanZScore.save()
            print("Stock: ", company_stock_symbol, ". Altman Z-Score:", altmanzscore)
        else:
            print("Stock: ", company_stock_symbol, ". Could not store Altman Z-Score")
    except:
        print("Stock: ", company_stock_symbol, ". Error: ",sys.exc_info())


def run():
    #company_id = 23465
    #company_stock = "APT"
    #financial_data(company_id, company_stock, "2015", "1")

    get_companies = Company.objects.all()
    for company in get_companies:
        financial_data(company.id, company.symbol, "2016", "2") # TODO code currently takes first quarter. You can modify this

