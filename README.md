This project is part of my phd dissertation that I published in 2014.

Setup Instructions (in progress)

Setup
-----

1) install mysql, apache, python3, virtualenv

2) Setup mysql database
    create database finsentimentdb;
    create user 'financedbuser'@'localhost' identified by '<password>';
    grant all privileges on finsentimentdb.* to 'financedbuser'@'localhost';
    flush privileges;
   
3) setup and activate Python3 virtual environment
    mkdir {env-location} - (select the path where you want the virtual environment)
    run virtualenv --python=python3 {env-location}
    source {env-location}/bin/activate
    
4) install all project requirements (make sure that you are in the virtual environment
    pip install -r requirements.txt
	
5) download and configure the latest code from github 
    git clone https://github.com/hoteit/finSentiment.git
    
6) update project settings
    - setup a Twitter app at https://apps.twitter.com (make sure you have a Twitter account first)
    - get Consumer Key (API Key), Consumer Secret (API Secret), Access Token, 	Access Token Secret
    and add them in the appropriate location with the settings.py configuration file
    - update the settings.py file with finSentiment app location in PROJECT_ROOT 
    and the database password under DATABASES
    - you can also update the polling time and size for the companies from Twitter by changing
    tweets_polling_time & tweets_polling_size
       
7) setup the application and the database model (make sure to be inside the virtual environment) 
    ./manage.py makemigrations
	./manage.py migrate

8) setup apache for production server or you can prepare a local version (TODO : add instructions)


Django
------

from the django environment, create a super user in order to access the site administration.
Then add a new user with the username "system". This is needed to keep track of the automated 
user for extracting Twitter data.
	
Data Population
---------------
step 1 - extract the list of company and stock symbols from Nasdaq website. The script retrieves the stock symbols of all publicly-held companies in the United States 
and it also adds  major market information.
    ./manage.py runscript all_company_nasdaqcom_importer --settings=finSentiment.local_settings

step 2- run the script below to populate the financial data of the firms using last quarterly 
data extracted from MorningStar.com and Yahoo Finance, calculates Altman Z-Score,
and stores the results into the database.
    ./manage.py runscript company_financials_extract --settings=finSentiment.local_settings
    
step 3 - run the script below that first queries the list of companies' stock symbols in the database.
It then picks up on an iterative basis a sample set of stock symbols to search for on Twitter in real-time streaming. 
Tweets associated with the stocks are then stored in the TwitterText database. 
   ./manage.py runscript company_tweets_collect -v3 --settings=finSentiment.local_settings
 


