__author__ = 'tarek'
### the script will retreive the financials from the database for each of the firms, calculate altman zscore
### and upload it into the database
import sys
import re

from twitterSentiment.models import Company, CompanyFinancials, CompanyAltmanZscore
# add some more to powers as necessary
import sys
def largenumbers(numstring):
	powers = {'B': 10 ** 9, 'M': 10 ** 6, 'T': 10 ** 12}
	try:
		numberregex = re.match("(\w.*?)([B|M|T])", numstring)
		decimal = numberregex.group(1)
		large = numberregex.group(2)
		return float(decimal) * powers[large]
	except:
		print (sys.exc_info())
		return numstring

def run():
	companies = Company.objects.filter()
	if companies is not None:
		for company in companies:
			try:
				companyFinancials = CompanyFinancials.objects.get(company__id = company.id, year="2014", quarter="3")
				current_assets = int(companyFinancials.current_assets)
				current_liability = int(companyFinancials.current_liability)
				working_capital = current_assets - current_liability
				total_assets = int(companyFinancials.total_assets)
				total_liability = int(companyFinancials.total_liability)
				retained_earnings = int(companyFinancials.retained_earnings)
				ebitda = int(companyFinancials.ebitda)
				market_capital = largenumbers(companyFinancials.market_capital)
				stockprice = float(companyFinancials.stockprice)
				sales = int(companyFinancials.sales)
				altmanX1 = working_capital / total_assets
				altmanX2 = retained_earnings / total_assets
				altmanX3 = ebitda / total_assets
				altmanX4 = market_capital /total_liability
				altmanX5 = sales / total_assets

				z=(1.2*altmanX1) + (1.4*altmanX2) + (3.3*altmanX3) + (0.6*altmanX4) + (0.999*altmanX5)

				print("current assets:", current_assets)
				print("current liability:", current_liability)
				print("total assets:", total_assets)
				print("total liability:", total_liability)
				print("retained earnings:", retained_earnings)
				print("ebitda:", ebitda)
				print("market capital:", market_capital)
				print("stock price:", stockprice)
				print("sales:", sales)
				print("x1:", altmanX1, "x2:",altmanX2, "x3:", altmanX3, "x4:",altmanX4, "x5:",altmanX5)
				print("Z Score: ", z)
				companyAltmanZscore = CompanyAltmanZscore(company_id=company.id, company_financials_id=companyFinancials.id, zscore=round(z,3))
				companyAltmanZscore.save()
				#sudo wait = input("press ENTER to continue")
			except:
				z=0
				print("error:", sys.exc_info())


