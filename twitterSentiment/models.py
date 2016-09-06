from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    # Each company under analysis
    symbol = models.CharField('Stock Symbol', max_length=10)
    name = models.CharField('Company Name', max_length=100)
    lastSale = models.DecimalField('Last Sale', max_digits=24, decimal_places=4, null=True, blank=True)
    marketCap = models.DecimalField('Market Cap', max_digits=24, decimal_places=4, null=True, blank=True)
    adrTso =  models.CharField('Adr Tso', max_length=20, null=True, blank=True)
    ipoYear = models.CharField('IPO Year', max_length=4, null=True, blank=True)
    sector = models.CharField('Sector', max_length=100, null=True, blank=True)
    industry = models.CharField('Industry', max_length=200, null=True, blank=True)
    summaryQuote = models.CharField('Summary Quote', max_length=200, null=True, blank=True)
    exchange = models.CharField('Stock Exchange', max_length=10, null=True, blank=True)
    date_extracted = models.DateTimeField('Date extracted', null=True, blank=True)
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def __str__(self):
        return self.name+'('+self.symbol+')'


class CompanyFinancials(models.Model):
    company=models.ForeignKey(Company)
    quarter=models.CharField('Quarter', max_length=1)
    year = models.CharField('Year', max_length=4)
    total_assets = models.DecimalField('Total Assets', max_digits=24, decimal_places=4, null=True, blank=True)
    total_liability = models.DecimalField('Total Liability', max_digits=24, decimal_places=4, null=True, blank=True)
    current_assets = models.DecimalField('Current Assets',max_digits=24, decimal_places=4, null=True, blank=True)
    current_liability = models.DecimalField('Current Liability', max_digits=24, decimal_places=4, null=True, blank=True)
    retained_earnings = models.DecimalField('Retained Earnings',max_digits=24, decimal_places=4, null=True, blank=True)
    market_capital = models.DecimalField('Market Capital',max_digits=24, decimal_places=4, null=True, blank=True)
    ebitda = models.DecimalField('EBITDA',max_digits=24, decimal_places=4, null=True, blank=True)
    sales = models.DecimalField('Sales',max_digits=24, decimal_places=4, null=True, blank=True)
    stockprice = models.DecimalField('Last Stock Price', max_digits=24, decimal_places=4, null=True, blank=True)
    date_extracted = models.DateTimeField('Date extracted', null=True, blank=True)

    class Meta:
        verbose_name = "Company Financial"
        verbose_name_plural = "Company Financials"

    def __str__(self):
        return self.company.name+" "+self.quarter+" - "+self.year


class CompanyKeyStats(models.Model):
    company=models.ForeignKey(Company)
    marketcap = models.DecimalField('Market Cap',  max_digits=24, decimal_places=4, null=True, blank=True)
    marketcap_term = models.DecimalField('Market Cap Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    enterprisevalue = models.DecimalField('Enterprise Value',  max_digits=24, decimal_places=4, null=True, blank=True)
    enterprisevalue_term = models.DecimalField('Enterprise Value Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    trailingpe = models.DecimalField('Trailing PE',  max_digits=24, decimal_places=4, null=True, blank=True)
    trailingpe_term = models.DecimalField('Trailing Pe Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    forwardpe = models.DecimalField('Forward PE',  max_digits=24, decimal_places=4, null=True, blank=True)
    forwardpe_term = models.DecimalField('Forward PE Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    pegratio = models.DecimalField('PEG Ratio',  max_digits=24, decimal_places=4, null=True, blank=True)
    pegratio_term = models.DecimalField('PEG Ratio Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    pricesales = models.DecimalField('Price Sales',  max_digits=24, decimal_places=4, null=True, blank=True)
    pricesales_term = models.DecimalField('Price Sales Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    pricebook = models.DecimalField('Price Book',  max_digits=24, decimal_places=4, null=True, blank=True)
    pricebook_term = models.DecimalField('Price Book Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    enterprisevaluerevenue = models.DecimalField('Enterprise Value Revenue',  max_digits=24, decimal_places=4, null=True, blank=True)
    enterprisevaluerevenue_term = models.DecimalField('Enterprise Value Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    enterprisevalueebitda = models.DecimalField('Enterprise Value Ebitda',  max_digits=24, decimal_places=4, null=True, blank=True)
    enterprisevalueebitda_term = models.DecimalField('Enterprise Value Ebitda Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    fiscalyearends= models.DecimalField('Fiscal Year Ends',  max_digits=24, decimal_places=4, null=True, blank=True)
    mostrecentquarter= models.DecimalField('Most Recent Quarter',  max_digits=24, decimal_places=4, null=True, blank=True)
    profitmargin= models.DecimalField('Profit Margin',  max_digits=24, decimal_places=4, null=True, blank=True)
    profitmargin_term= models.DecimalField('Profit Margin Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    operatingmargin= models.DecimalField('Operating Margin',  max_digits=24, decimal_places=4, null=True, blank=True)
    operatingmargin_term= models.DecimalField('Operating Margin Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    returnonassets= models.DecimalField('Return On Assets',  max_digits=24, decimal_places=4, null=True, blank=True)
    returnonassets_term= models.DecimalField('Return on Assets Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    returnonequity= models.DecimalField('Return On Equity',  max_digits=24, decimal_places=4, null=True, blank=True)
    returnonequity_term= models.DecimalField('Return on Equity Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    revenue = models.DecimalField('Revenue',  max_digits=24, decimal_places=4, null=True, blank=True)
    revenue_term = models.DecimalField('Revenue Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    revenuepershare = models.DecimalField('Revenue Per Share',  max_digits=24, decimal_places=4, null=True, blank=True)
    revenuepershare_term = models.DecimalField('Revenue Per Share Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    quarterlyrevenuegrowth = models.DecimalField('Quarterly Revenue Growth',  max_digits=24, decimal_places=4, null=True, blank=True)
    quarterlyrevenuegrowth_term = models.DecimalField('Quarterly Revenue Growth Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    grossprofit = models.DecimalField('Gross Profit',  max_digits=24, decimal_places=4, null=True, blank=True)
    grossprofit_term = models.DecimalField('Gross Profit Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    ebitda = models.DecimalField('Ebitda',  max_digits=24, decimal_places=4, null=True, blank=True)
    ebitda_term = models.DecimalField('Ebitda Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    netincomeavltocommon = models.DecimalField('Net Income Available to Common',  max_digits=24, decimal_places=4, null=True, blank=True)
    netincomeavltocommon_term = models.DecimalField('Net Income Available to Common Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    dilutedeps = models.DecimalField('Diluted EPS',  max_digits=24, decimal_places=4, null=True, blank=True)
    dilutedeps_term = models.DecimalField('Diluted EPS Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    quarterlyearningsgrowth = models.DecimalField('Quarterly Earnings Growth',  max_digits=24, decimal_places=4, null=True, blank=True)
    quarterlyearningsgrowth_term = models.DecimalField('Quarterly Earnings Growth Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    totalcash = models.DecimalField('Total Cash',  max_digits=24, decimal_places=4, null=True, blank=True)
    totalcash_term = models.DecimalField('Total Cash Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    totalcashpershare = models.DecimalField('Total Cash per Share',  max_digits=24, decimal_places=4, null=True, blank=True)
    totalcashpershare_term = models.DecimalField('Total Cash per Share Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    totaldebt = models.DecimalField('Total Debt',  max_digits=24, decimal_places=4, null=True, blank=True)
    totaldebt_term = models.DecimalField('Total Debt Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    totaldebtequity = models.DecimalField('Total Debt Equity',  max_digits=24, decimal_places=4, null=True, blank=True)
    totaldebtequity_term = models.DecimalField('Total Debt Equity Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    currentratio = models.DecimalField('Current Ratio',  max_digits=24, decimal_places=4, null=True, blank=True)
    currentratio_term = models.DecimalField('Current Ratio Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    bookvaluepershare = models.DecimalField('Book Value Per Share',  max_digits=24, decimal_places=4, null=True, blank=True)
    bookvaluepershare_term = models.DecimalField('Book Value Per Share Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    operatingcashflow = models.DecimalField('Operating Cash Flow',  max_digits=24, decimal_places=4, null=True, blank=True)
    operatingcashflow_term = models.DecimalField('Operating Cash Flow Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    leveredfreecashflow = models.DecimalField('Levered Free Cash Flow',  max_digits=24, decimal_places=4, null=True, blank=True)
    leveredfreecashflow_term = models.DecimalField('Levered Free Cash Flow Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    beta = models.DecimalField('Beta',  max_digits=24, decimal_places=4, null=True, blank=True)
    p52weekchange = models.DecimalField('p52weekchange',  max_digits=24, decimal_places=4, null=True, blank=True)
    sp500p52weekchange = models.DecimalField('sp500p52weekchange',  max_digits=24, decimal_places=4, null=True, blank=True)
    p52weekhigh = models.DecimalField('p52weekhigh',  max_digits=24, decimal_places=4, null=True, blank=True)
    p52weekhigh_term = models.DecimalField('p52weekhigh Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    p52weeklow = models.DecimalField('p52weeklow',  max_digits=24, decimal_places=4, null=True, blank=True)
    p52weeklow_term = models.DecimalField('p52weeklow Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    p50daymovingaverage = models.DecimalField('p50daymovingaverage',  max_digits=24, decimal_places=4, null=True, blank=True)
    p200daymovingaverage = models.DecimalField('p200daymovingaverage', max_digits=24, decimal_places=4, null=True, blank=True)
    averagevolume = models.DecimalField('Average Volume',  max_digits=24, decimal_places=4, null=True, blank=True)
    averagevolume_term = models.DecimalField('Average Volume Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    sharesoutstanding= models.DecimalField('Shares Outstanding',  max_digits=24, decimal_places=4, null=True, blank=True)
    sfloat=models.DecimalField('Float',  max_digits=24, decimal_places=4, null=True, blank=True)
    percenthldbyinsiders=models.DecimalField('Percent Held by Insiders',  max_digits=24, decimal_places=4, null=True, blank=True)
    percenthldbyinstitutions=models.DecimalField('Percent Held by Institutions',  max_digits=24, decimal_places=4, null=True, blank=True)
    sharesshort=models.DecimalField('Shares Short', max_digits=24, decimal_places=4, null=True, blank=True)
    shareshort_term=models.DecimalField('Shares Short Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    shortratio=models.DecimalField('Short Ratio',  max_digits=24, decimal_places=4, null=True, blank=True)
    shortratio_term=models.DecimalField('Short Ratio Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    shortpercentfloat=models.DecimalField('Short Percentage Float',  max_digits=24, decimal_places=4, null=True, blank=True)
    shortpercentfloat_term=models.DecimalField('Short Percentage Float Term',  max_digits=24, decimal_places=4, null=True, blank=True)
    forwardannualdividentrate= models.DecimalField('forwardannualdividentrate',  max_digits=24, decimal_places=4, null=True, blank=True)
    forwardannualdividentyield= models.DecimalField('forwardannualdividentyield',  max_digits=24, decimal_places=4, null=True, blank=True)
    trailingannualdividentrate= models.DecimalField('trailingannualdividentrate',  max_digits=24, decimal_places=4, null=True, blank=True)
    trailingannualdividentyield= models.DecimalField('trailingannualdividentyield',  max_digits=24, decimal_places=4, null=True, blank=True)
    p_5yearaveragedivident= models.DecimalField('p_5yearaveragedivident',  max_digits=24, decimal_places=4, null=True, blank=True)
    payoutratio= models.DecimalField('payoutratio',  max_digits=24, decimal_places=4, null=True, blank=True)
    dividentrate= models.DecimalField('dividentrate',  max_digits=24, decimal_places=4, null=True, blank=True)
    ex_dividentrate= models.DecimalField('ex_dividentrate',  max_digits=24, decimal_places=4, null=True, blank=True)
    lastsplitfactor= models.DecimalField('lastsplitfactor',  max_digits=24, decimal_places=4, null=True, blank=True)
    lastsplitfactor_term= models.DecimalField('lastsplitfactor_term',  max_digits=24, decimal_places=4, null=True, blank=True)
    lastsplitdate= models.DateField('lastsplitdate',  null=True, blank=True)



class TwitterText(models.Model):
    # Each sentiment related to the companies under analysis and captured from the social media platforms
    twitter_userid = models.CharField('Twitter User ID', max_length=255, null=True, blank=True)
    twitter_user_name = models.CharField('Social User Name', max_length=100, null=True, blank=True)
    twitter_text = models.CharField('Social Updates', max_length=1024, null=True, blank=True)
    twitter_textid = models.CharField('Message Id', max_length=255, null=True, blank=True)
    twitter_text_timestamp = models.DateTimeField('Message Timestamp', null=True, blank=True)
    twitter_text_keyword = models.CharField('Keyword', max_length=1000, null=True, blank=True)
    twitter_for_training = models.IntegerField('training value', default=9) #9 untrained #0: trained dataset,1: dev-test dataset, 2: test dataset #4 applied dataset
    twitter_sentiment = models.IntegerField('sentiment', default=2)
    twitter_retweeted = models.BooleanField('retweeted', default=False)
    training_user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        verbose_name = "Twitter Text"
        verbose_name_plural = "Twitter Texts"

    def __str__(self):
        return self.twitter_text+" keyword: "+self.twitter_text_keyword


class CompanyAltmanZscore(models.Model):
    company=models.ForeignKey(Company)
    company_financials = models.ForeignKey(CompanyFinancials)
    zscore = models.DecimalField("Altman Z-Score", max_digits=10 ,decimal_places=4, null=True,blank=True)
    date_updated = models.DateTimeField('Date Calculated', auto_now=True)

    class Meta:
        verbose_name = "Altman Score"
        verbose_name_plural = "Altman Scores"

    def __str__(self):
        return self.company.name+" - zscore:"+self.zscore


class CompanySentiment(models.Model):
    company = models.ForeignKey(Company)
    twitter_text = models.ForeignKey(TwitterText)
    sentiment_prob_very_negative = models.DecimalField('Very Negative Probability', max_digits=24, decimal_places=4, null=True, blank=True)
    sentiment_prob_negative = models.DecimalField('Negative Probability', max_digits=24, decimal_places=4, null=True, blank=True)
    sentiment_prob_neutral = models.DecimalField('Neutral Probability', max_digits=24, decimal_places=4, null=True, blank=True)
    sentiment_prob_positive = models.DecimalField('Positive Probability', max_digits=24, decimal_places=4, null=True, blank=True)
    sentiment_prob_very_positive = models.DecimalField('Very Positive Probability', max_digits=24, decimal_places=4, null=True, blank=True)
    sentiment_root_value = models.DecimalField('Sentiment', max_digits=24, decimal_places=4, null=True, blank=True)
    date_updated = models.DateTimeField('Date Calculated', auto_now=True)

    class Meta:
        verbose_name = "Company Sentiment"
        verbose_name_plural = "Company Sentiments"

    def __str__(self):
        return self.company+" - tweet: "+self.twitter_text.id+" - sentiment: "+self.sentiment_root_value


class CompanyQuoteHistory(models.Model):
    company=models.ForeignKey(Company)
    date = models.DateField('Quote Date',null=True, blank=True)
    open=models.DecimalField('Open',max_digits=24, decimal_places=4, null=True, blank=True)
    high = models.DecimalField('High', max_digits=24, decimal_places=4, null=True, blank=True)
    low = models.DecimalField('Low', max_digits=24, decimal_places=4, null=True, blank=True)
    close = models.DecimalField('Close',max_digits=24, decimal_places=4, null=True, blank=True)
    volume = models.DecimalField('Volume',max_digits=24, decimal_places=4,  null=True, blank=True)
    adjs_close = models.DecimalField('Adj Close',max_digits=24, decimal_places=4, null=True, blank=True)
    symbol = models.CharField('Symbol', null=True, blank=True, max_length=10)

    class Meta:
        verbose_name = "Company Quote History"
        verbose_name_plural = "Company Quote History"

    def __str__(self):
        return self.company.name+self.date+" trend: "+(self.close - self.open)


class CompanyStocksSentimentHistory(models.Model):
    company=models.ForeignKey(Company)
    symbol = models.CharField('Stock Symbol',max_length=10, null=True, blank=True )
    date = models.DateField('Quote Date',null=True, blank=True)
    tweet_count =   models.IntegerField('Tweets', null=True, blank=True)
    sentiment = models.IntegerField('Sentiment', null=True, blank=True)
    stockopen = models.DecimalField('Stock Open',max_digits=24, decimal_places=4,  null=True, blank=True)
    stockclose = models.DecimalField('Stock Close',max_digits=24, decimal_places=4, null=True, blank=True)
    stockdirection = models.IntegerField('Stock Direction', null=True, blank=True)

    class Meta:
        verbose_name = "Company Tweet Quote "
        verbose_name_plural = "Company Tweet Quotes"

    def __str__(self):
        return self.company.name+" - tweet id: "+self.twitter_text.id+" "+self.date+" trend: "+(self.close - self.open)
