import pandas as pd
import urllib
import time
import sys
from twitterSentiment.models import CompanyKeyStats
# script that loops over all the public companies in allpubliccomp.csv, extracts the financials using YQL then store the
#the results in a new csv file

#note the financials are annual

count = 1
total = 1


def stat(bs_json, astat, content):
   try:
        if content == 'content':
            return bs_json["query"]["results"]["stats"][astat]['content']
        elif content == 'term':
            return bs_json["query"]["results"]["stats"][astat]['term']
        else:
            return bs_json["query"]["results"]["stats"][astat]
   except:
       return

def keystats_variables1(stock):
    return (stock)

def keystats_variables(stock):
    #function to query Yahoo YQL and return the financial financialdata for a stock based on stock symbol.
    #the variables are selected according to Altman Z-Score
    stock = stock.strip('$')
    marketcap = ""
    marketcap_term = ""
    enterprisevalue = ""
    enterprisevalue_term = ""
    trailingpe = ""
    trailingpe_term = ""
    forwardpe = ""
    forwardpe_term = ""
    pegratio = ""
    pegratio_term = ""
    pricesales = ""
    pricesales_term = ""
    pricebook = ""
    pricebook_term = ""
    enterprisevaluerevenue = ""
    enterprisevaluerevenue_term = ""
    enterprisevalueebitda = ""
    enterprisevalueebitda_term = ""
    fiscalyearends = ""
    mostrecentquarter = ""
    profitmargin = ""
    profitmargin_term = ""
    operatingmargin = ""
    operatingmargin_term = ""
    returnonassets = ""
    returnonassets_term = ""
    returnonequity = ""
    returnonequity_term = ""
    revenue = ""
    revenue_term = ""
    revenuepershare = ""
    revenuepershare_term = ""
    quarterlyrevenuegrowth = ""
    quarterlyrevenuegrowth_term = ""
    grossprofit = ""
    grossprofit_term = ""
    ebitda = ""
    ebitda_term = ""
    netincomeavltocommon = ""
    netincomeavltocommon_term = ""
    dilutedeps = ""
    dilutedeps_term = ""
    quarterlyearningsgrowth = ""
    quarterlyearningsgrowth_term = ""
    totalcash = ""
    totalcash_term = ""
    totalcashpershare = ""
    totalcashpershare_term = ""
    totaldebt = ""
    totaldebt_term = ""
    totaldebtequity = ""
    totaldebtequity_term = ""
    currentratio = ""
    currentratio_term = ""
    bookvaluepershare = ""
    bookvaluepershare_term = ""
    operatingcashflow = ""
    operatingcashflow_term = ""
    leveredfreecashflow = ""
    leveredfreecashflow_term = ""
    beta = ""
    p52weekchange = ""
    sp500p52weekchange = ""
    p52weekhigh = ""
    p52weekhigh_term = ""
    p52weeklow = ""
    p52weeklow_term = ""
    p50daymovingaverage = ""
    p200daymovingaverage = ""
    averagevolume = ""
    averagevolume_term = ""
    sharesoutstanding = ""

    sfloat = ""
    percenthldbyinsiders = ""
    percenthldbyinstitutions = ""
    sharesshort = ""
    shareshort_term = ""
    shortratio = ""
    shortratio_term = ""
    shortpercentfloat = ""
    shortpercentfloat_term = ""
    forwardannualdividentrate = ""
    forwardannualdividentyield = ""
    trailingannualdividentrate = ""
    trailingannualdividentyield = ""
    p_5yearaveragedivident = ""
    payoutratio = ""
    dividentrate = ""
    ex_dividentrate = ""
    lastsplitfactor = ""
    lastsplitfactor_term = ""
    lastsplitdate = ""

    try:
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        #extract financialdata from balance sheet
        yql_bs_query = "select * from yahoo.finance.keystats where symbol = '" + stock + "'"
        yql_bs_url = baseurl + urllib.parse.urlencode({
        'q': yql_bs_query}) + "&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
        bs_json = pd.io.json.read_json(yql_bs_url)
        if bs_json["query"]["results"] is not None:
            marketcap = stat(bs_json, "MarketCap", "content")
            marketcap_term = stat(bs_json, "MarketCap", "term")
            enterprisevalue = stat(bs_json, "EnterpriseValue", "content")
            enterprisevalue_term = stat(bs_json, "EnterpriseValue", "term")
            trailingpe = stat(bs_json, "TrailingPE", "content")
            trailingpe_term = stat(bs_json, "TrailingPE", "term")
            forwardpe = stat(bs_json, "ForwardPE", "content")
            forwardpe_term = stat(bs_json, "ForwardPE", "term")
            pegratio = stat(bs_json, "PEGRatio", "content")
            pegratio_term = stat(bs_json, "PEGRatio", "term")
            pricesales = stat(bs_json, "PriceSales", "content")
            pricesales_term = stat(bs_json, "PriceSales", "term")
            pricebook = stat(bs_json, "PriceBook", "content")
            pricebook_term = stat(bs_json, "PriceBook", "term")
            enterprisevaluerevenue = stat(bs_json, "EnterpriseValueRevenue", "content")
            enterprisevalue_term = stat(bs_json, "EnterpriseValueRevenue", "term")
            enterprisevalueebitda = stat(bs_json, "EnterpriseValueEBITDA", "content")
            enterprisevalueebitda_term = stat(bs_json, "EnterpriseValueEBITDA", "term")
            fiscalyearends = stat(bs_json, "FiscalYearEnds","none")
            mostrecentquarter = stat(bs_json, "MostRecentQuarter", "content")
            profitmargin = stat(bs_json, "ProfitMargin", "content")
            profitmargin_term = stat(bs_json, "ProfitMargin", "term")
            operatingmargin = stat(bs_json, "OperatingMargin", "content")
            operatingmargin_term = stat(bs_json, "OperatingMargin", "term")
            returnonassets = stat(bs_json, "ReturnonAssets", "content")
            returnonassets_term = stat(bs_json, "ReturnonAssets", "term")
            returnonequity = stat(bs_json, "ReturnonEquity", "content")
            returnonequity_term = stat(bs_json, "ReturnonEquity", "term")
            revenue = stat(bs_json, "Revenue", "content")
            revenue_term = stat(bs_json, "Revenue", "term")
            revenuepershare = stat(bs_json, "RevenuePerShare", "content")
            revenuepershare_term = stat(bs_json, "RevenuePerShare", "term")
            quarterlyrevenuegrowth = stat(bs_json, "QtrlyRevenueGrowth", "content")
            quarterlyearningsgrowth_term = stat(bs_json, "QtrlyRevenueGrowth", "term")
            grossprofit = stat(bs_json, "GrossProfit", "content")
            grossprofit_term = stat(bs_json, "GrossProfit", "term")
            ebitda = stat(bs_json, "EBITDA", "content")
            ebitda_term = stat(bs_json, "EBITDA", "term")
            netincomeavltocommon = stat(bs_json, "NetIncomeAvltoCommon", "content")
            netincomeavltocommon_term = stat(bs_json, "NetIncomeAvltoCommon", "term")
            dilutedeps = stat(bs_json, "DilutedEPS", "content")
            dilutedeps_term = stat(bs_json, "DilutedEPS", "term")
            quarterlyearningsgrowth = stat(bs_json, "QtrlyEarningsGrowth", "content")
            quarterlyearningsgrowth_term = stat(bs_json, "QtrlyEarningsGrowth", "term")
            totalcash = stat(bs_json, "TotalCash", "content")
            totalcash_term = stat(bs_json, "TotalCash", "term")
            totalcashpershare = stat(bs_json, "TotalCashPerShare", "content")
            totalcashpershare_term = stat(bs_json, "TotalCashPerShare", "term")
            totaldebt = stat(bs_json, "TotalDebt", "content")
            totaldebt_term = stat(bs_json, "TotalDebt", "term")
            totaldebtequity = stat(bs_json, "TotalDebtEquity", "content")
            totaldebtequity_term = stat(bs_json, "TotalDebtEquity", "term")
            currentratio = stat(bs_json, "CurrentRatio", "content")
            currentratio_term = stat(bs_json, "CurrentRatio", "term")
            bookvaluepershare = stat(bs_json, "BookValuePerShare", "content")
            bookvaluepershare_term = stat(bs_json, "BookValuePerShare", "term")
            operatingcashflow = stat(bs_json, "OperatingCashFlow", "content")
            operatingcashflow_term = stat(bs_json, "OperatingCashFlow", "term")
            leveredfreecashflow = stat(bs_json, "LeveredFreeCashFlow", "content")
            leveredfreecashflow_term = stat(bs_json, "LeveredFreeCashFlow", "term")
            beta = stat(bs_json, "Beta","none")
            p52weekchange = stat(bs_json, "p_52_WeekChange","none")
            sp500p52weekchange = stat(bs_json, "SP50052_WeekChange","none")
            p52weekhigh = stat(bs_json, "p_52_WeekHigh", "content")
            p52weekhigh_term = stat(bs_json, "p_52_WeekHigh", "term")
            p52weeklow = stat(bs_json, "p_52_WeekLow", "content")
            p52weeklow_term = stat(bs_json, "p_52_WeekLow", "term")
            p50daymovingaverage = stat(bs_json, "p_50_DayMovingAverage","none")
            p200daymovingaverage = stat(bs_json, "p_200_DayMovingAverage","none")
            averagevolume = stat(bs_json, "AvgVol", "none")
            averagevolume_term = stat(bs_json, "AvgVol", "none")
            sharesoutstanding = stat(bs_json, "SharesOutstanding","none")
            sfloat = stat(bs_json, "Float","none")
            percenthldbyinsiders = stat(bs_json, "PercentageHeldbyInsiders","none")
            percenthldbyinstitutions = stat(bs_json, "PercentageHeldbyInstitutions","none")
            sharesshort = stat(bs_json, "SharesShort", "none")
            shareshort_term = stat(bs_json, "SharesShort", "none")
            shortratio = stat(bs_json, "ShortRatio", "content")
            shortratio_term = stat(bs_json, "ShortRatio", "term")
            shortpercentfloat = stat(bs_json, "ShortPercentageofFloat", "content")
            shortpercentfloat_term = stat(bs_json, "ShortPercentageofFloat", "term")
            forwardannualdividentrate = stat(bs_json, "ForwardAnnualDividendRate","none")
            forwardannualdividentyield = stat(bs_json, "ForwardAnnualDividendYield","none")
            trailingannualdividentyield = stat(bs_json, "TrailingAnnualDividendYield","none")
            p_5yearaveragedivident = stat(bs_json, "p_5YearAverageDividendYield","none")
            payoutratio = stat(bs_json, "PayoutRatio","none")
            dividentrate = stat(bs_json, "DividendDate","none")
            ex_dividentrate = stat(bs_json, "Ex_DividendDate","none")
            lastsplitfactor = stat(bs_json, "LastSplitFactor", "content")
            lastsplitfactor_term = stat(bs_json, "LastSplitFactor", "term")
            lastsplitdate = stat(bs_json, "LastSplitDate","none")
    except:
        print("error on ", stock, ". Error message", sys.exc_info())
    global count
    count = count + 1
    global total
    print("\n", count, "/", total, ":\n Stock:", stock, ":"
          , "* marketcap: ", marketcap
          , "* marketcap_term : ", marketcap_term
          , "* enterprisevalue : ", enterprisevalue
          , "* enterprisevalue_term : ", enterprisevalue_term
          , "* trailingpe : ", trailingpe
          , "* trailingpe_term : ", trailingpe_term
          , "* forwardpe : ", forwardpe
          , "* forwardpe_term : ", forwardpe_term
          , "* pegratio : ", pegratio
          , "* pegratio_term : ", pegratio_term
          , "* pricesales : ", pricesales
          , "* pricesales_term : ", pricesales_term
          , "* pricebook : ", pricebook
          , "* pricebook_term : ", pricebook_term
          , "* enterprisevaluerevenue : ", enterprisevaluerevenue
          , "* enterprisevalue_term : ", enterprisevalue_term
          , "* enterprisevalueebitda : ", enterprisevalueebitda
          , "* enterprisevalueebitda_term : ", enterprisevalueebitda_term
          , "* fiscalyearends : ", fiscalyearends
          , "* mostrecentquarter : ", mostrecentquarter
          , "* profitmargin : ", profitmargin
          , "* profitmargin_term : ", profitmargin_term
          , "* operatingmargin : ", operatingmargin
          , "* operatingmargin_term : ", operatingmargin_term
          , "* returnonassets : ", returnonassets
          , "* returnonassets_term : ", returnonassets_term
          , "* returnonequity : ", returnonequity
          , "* returnonequity_term : ", returnonequity_term
          , "* revenue : ", revenue
          , "* revenue_term : ", revenue_term
          , "* revenuepershare : ", revenuepershare
          , "* revenuepershare_term : ", revenuepershare_term
          , "* quarterlyrevenuegrowth : ", quarterlyrevenuegrowth
          , "* quarterlyearningsgrowth_term : ", quarterlyearningsgrowth_term
          , "* grossprofit : ", grossprofit
          , "* grossprofit_term : ", grossprofit_term
          , "* ebitda : ", ebitda
          , "* ebitda_term : ", ebitda_term
          , "* netincomeavltocommon : ", netincomeavltocommon
          , "* netincomeavltocommon_term : ", netincomeavltocommon_term
          , "* dilutedeps : ", dilutedeps
          , "* dilutedeps_term : ", dilutedeps_term
          , "* quarterlyearningsgrowth : ", quarterlyearningsgrowth
          , "* quarterlyearningsgrowth_term : ", quarterlyearningsgrowth_term
          , "* totalcash : ", totalcash
          , "* totalcash_term : ", totalcash_term
          , "* totalcashpershare : ", totalcashpershare
          , "* totalcashpershare_term : ", totalcashpershare_term
          , "* totaldebt : ", totaldebt
          , "* totaldebt_term : ", totaldebt_term
          , "* totaldebtequity : ", totaldebtequity
          , "* totaldebtequity_term : ", totaldebtequity_term
          , "* currentratio : ", currentratio
          , "* currentratio_term : ", currentratio_term
          , "* bookvaluepershare : ", bookvaluepershare
          , "* bookvaluepershare_term : ", bookvaluepershare_term
          , "* operatingcashflow : ", operatingcashflow
          , "* operatingcashflow_term : ", operatingcashflow_term
          , "* leveredfreecashflow : ", leveredfreecashflow
          , "* leveredfreecashflow_term : ", leveredfreecashflow_term
          , "* beta : ", beta
          , "* p52weekchange : ", p52weekchange
          , "* sp500p52weekchange : ", sp500p52weekchange
          , "* p52weekhigh : ", p52weekhigh
          , "* p52weekhigh_term : ", p52weekhigh_term
          , "* p52weeklow : ", p52weeklow
          , "* p52weeklow_term : ", p52weeklow_term
          , "* p50daymovingaverage : ", p50daymovingaverage
          , "* p200daymovingaverage : ", p200daymovingaverage
          , "* averagevolume : ", averagevolume
          , "* averagevolume_term : ", averagevolume_term
          , "* sharesoutstanding : ", sharesoutstanding
          , "* sfloat: ", sfloat
          , "* percenthldbyinsiders: ", percenthldbyinsiders
          , "* percenthldbyinstitutions: ", percenthldbyinstitutions
          , "* sharesshort: ", sharesshort
          , "* shareshort_term: ", shareshort_term
          , "* shortratio: ", shortratio
          , "* shortratio_term: ", shortratio_term
          , "* shortpercentfloat: ", shortpercentfloat
          , "* shortpercentfloat_term: ", shortpercentfloat_term
          , "* forwardannualdividentrate: ", forwardannualdividentrate
          , "* forwardannualdividentyield: ", forwardannualdividentyield
          , "* trailingannualdividentrate: ", trailingannualdividentrate
          , "* trailingannualdividentyield: ", trailingannualdividentyield
          , "* p_5yearaveragedivident: ", p_5yearaveragedivident
          , "* payoutratio: ", payoutratio
          , "* dividentrate: ", dividentrate
          , "* ex_dividentrate: ", ex_dividentrate
          , "* lastsplitfactor: ", lastsplitfactor
          , "* lastsplitfactor_term: ", lastsplitfactor_term
          , "* lastsplitdate: ", lastsplitdate)

    return ([marketcap,
             marketcap_term,
             enterprisevalue,
             enterprisevalue_term,
             trailingpe,
             trailingpe_term,
             forwardpe,
             forwardpe_term,
             pegratio,
             pegratio_term,
             pricesales,
             pricesales_term,
             pricebook,
             pricebook_term,
             enterprisevaluerevenue,
             enterprisevalue_term,
             enterprisevalueebitda,
             enterprisevalueebitda_term,
             fiscalyearends,
             mostrecentquarter,
             profitmargin,
             profitmargin_term,
             operatingmargin,
             operatingmargin_term,
             returnonassets,
             returnonassets_term,
             returnonequity,
             returnonequity_term,
             revenue,
             revenue_term,
             revenuepershare,
             revenuepershare_term,
             quarterlyrevenuegrowth,
             quarterlyearningsgrowth_term,
             grossprofit,
             grossprofit_term,
             ebitda,
             ebitda_term,
             netincomeavltocommon,
             netincomeavltocommon_term,
             dilutedeps,
             dilutedeps_term,
             quarterlyearningsgrowth,
             quarterlyearningsgrowth_term,
             totalcash,
             totalcash_term,
             totalcashpershare,
             totalcashpershare_term,
             totaldebt,
             totaldebt_term,
             totaldebtequity,
             totaldebtequity_term,
             currentratio,
             currentratio_term,
             bookvaluepershare,
             bookvaluepershare_term,
             operatingcashflow,
             operatingcashflow_term,
             leveredfreecashflow,
             leveredfreecashflow_term,
             beta,
             p52weekchange,
             sp500p52weekchange,
             p52weekhigh,
             p52weekhigh_term,
             p52weeklow,
             p52weeklow_term,
             p50daymovingaverage,
             averagevolume,
             averagevolume_term,
             sharesoutstanding,
             sfloat,
             percenthldbyinsiders,
             percenthldbyinstitutions,
             sharesshort,
             shareshort_term,
             shortratio,
             shortratio_term,
             shortpercentfloat,
             shortpercentfloat_term,
             forwardannualdividentrate,
             forwardannualdividentyield,
             trailingannualdividentrate,
             trailingannualdividentyield,
             p_5yearaveragedivident,
             payoutratio,
             dividentrate,
             ex_dividentrate,
             lastsplitfactor,
             lastsplitfactor_term,
             lastsplitdate, ])

def run():
    try:
        firms_fin_location = "financialdata/allpubliccomp.csv"
        firms = pd.read_csv(firms_fin_location)
        total = len(firms.index)
        print(total)
        #print (keystats_variables("$VZ"))
        firms['keystats'] = firms['Symbol'].apply(keystats_variables)
        firms.to_csv('financialdata/keystats_results.csv')
    except:
        print("Error message", sys.exc_info())
