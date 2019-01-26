---
layout: post
title:  "Data Population"
date:   2016-09-28 19:25 -0500
categories: setup
permalink: /setup/datapopulation
---

After completing the [Installation](/finSentiment/setup/installation) step, the data population process is as follows:  

step 1 - extract the list of company and stock symbols from Nasdaq website. The script retrieves the stock symbols of all publicly-held companies in the United States 
and it also adds  major market information.
    
    ./manage.py runscript all_company_nasdaqcom_importer

step 2- run the script below to populate the financial data of the firms using last quarterly 
data extracted from MorningStar.com and Yahoo Finance, calculates Altman Z-Score,
and stores the results into the database.
    
    ./manage.py runscript company_financials_extract
    
step 3 - run the script below that first queries the list of companies stock symbols in the database.
It then picks up on an iterative basis a sample set of stock symbols to search for on Twitter in real-time streaming. 
Tweets associated with the stocks are then stored in the TwitterText database. 
   
    ./manage.py runscript company_tweets_collect
   
 
   
      
   