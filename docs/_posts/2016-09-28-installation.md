---
layout: post
title:  "Installation Process"
date:   2016-09-28 17:57 -0500
categories: setup
permalink: /setup/installation
---

The application is mostly developed in Python using [Tweepy](http://www.tweepy.org) to extract tweets from Twitter, [Django](https://djangoproject.com) for the portal and to help train the machine learning algorithm, [Stanford Core NLP](https://stanfordnlp.github.io/CoreNLP) for the sentiment analysis, and various Python tools including [IPython](http://ipython.org/), [Pandas](http://pandas.pydata.org/), and [Django-extensions](https://github.com/django-extensions/django-extensions).

The requirements to setup the system is as follows. Note that it is assumed that we are installing on a Debian instance.

1) Setup a Debian instance on a local machine, a Docker container, or a cloud instance. Then run:
     
     sudo apt-get update
     sudo apt-get upgrade

2) Install python dev, mysql server and client

    sudo apt-get install mysql-server mysqlclient python-dev libmysqlclient-dev

Setup the root account and then run `sudo mysql_secure_installation`

3) make sure that Python3 is installed and install VirtualEnv so as to isolate our Python environment for the app only.
`sudo apt-get install virtualenv`

4) install apache2, and apache2 python modules

     sudo apt-get install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert libapache2-mod-wsgi

Now that you have the basic components installed, we will go ahead and setup the code, the code dependencies, and make the necessary configurations. 

* I am assuming that you completed the steps above. Next is to setup the code.
1) Identify the location where you want the code to be setup. I will asssume that we will create it under /var/www/apps and with permissions correctly set. I personally have done the following
`sudo install -d -o tarek -g tarek /var/www/apps` (created the directory and updated the ownership for my settings)

Assuming that the directory is **/var/www/apps** and we are in that directory, `cd /var/www/apps`, let download the code.
2) `git clone https://github.com/hoteit/finSentiment`  (TODO: this will be replaced with some type of code packaging in the future)

3) Setup Python virtual environment and install the python requirements for the project Note: I am assuming your are in /var/www/apps/finSentiment

     virtualenv -p /usr/bin/python3 env
     source env/bin/activate
     (env) pip install -r requirements.txt

Note:  if you get specific errors when installing the requirements, check the following:
If you get errors when running `pip install -r requirements.txt`, here is what you can do
* **x86_64-linux-gnu-gcc: not found**, run `sudo apt-get install build-essentials`
* **mysql_config not found**, run `sudo apt-get install libmysqlclient-dev`
* **python.h not found**, run  `sudo apt-get install python3-dev`


4) Setup mysql database and user account for Django

     mysql -u root -p
     mysql> create database finSentimentDB;
     mysql> create user 'finSentimentUser'@'localhost' identified by '*********' 
     mysql> grant all privileges on finSentimetnDB.* to 'finSentimentUser'@'localhost';
     mysql> flush privileges;

5) Update **finSentiment/settings.py** with the following information:

    PROJECT_ROOT = '[location of the app]' in our case PROJECT_ROOT = '/var/www/apps/finSentiment'
    {....}
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finsentimentDB', # insert database name
        'USER': 'finSentimentUser', # insert database user name
        'PASSWORD': '******', # insert database password
        'HOST': '',
        'PORT': '',
        'OPTIONS': {'charset': 'utf8mb4'},
        'CONN_MAX_AGE': None,
    }

6) Run Django migration to update the database (make sure that you are within the virtual environment.)
   
    (env)  ./manage.py makemigrations
    (env)  ./manage.py migrate
 
7) Setup Apache page for Django
    
    a. create the file under /var/apache2/sites-available/finSentiment.conf with the following text

     <VirtualHost *:80>
        ServerName finsentiment.nkey.io
        ServerAdmin tarek@nkey.io

        LogLevel error
        ErrorLog ${APACHE_LOG_DIR}/finsentiment-error.log
        CustomLog ${APACHE_LOG_DIR}/finsentiment-access.log combined

        WSGIDaemonProcess finsentiment.nkey.io python-path=/var/www/apps/finSentiment:/var/www/apps/finSentiment/env/lib/python3.4/site-packages
       WSGIProcessGroup finsentiment.nkey.io

       WSGIScriptAlias / /var/www/apps/finSentiment/apache/wsgi.py process-group=finsentiment.nkey.io
       DirectoryIndex index.html index.php
       DocumentRoot /var/www/apps/finSentiment/html
       <Directory /var/www/apps/finSentiment/html>
               Require all granted
       </Directory>
        <Directory /var/www/apps/finSentiment/apache>
                Require all granted
       </Directory>
    </VirtualHost>
    
 b. activate the virtual directory `a2ensite finSentiment.conf' and restart the Apache2 instance
 c. update the file /var/www/apps/finSentiment/apache/wsgi.py with the location of your Python environment and the code
 d/ 

8) You now need to setup a Twitter application account. Access https://apps.twitter.com/ , and select 
**Create New App** Follow the instructions to setup Consumer Key (API Key), Consumer Secret(API Secret), Access Token, and Access Token Secret
Once you do, copy and paste the values in *finSentiment/settings.py:

    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

Once you are done, you can go ahead with the [Data Population](/finSentiment/setup/datapopulation) process
 

9) Setup Django administration page, create a super user and add a new user called `system`
 
    (env) ./manage createsuperuser
    then access `http://(site)/finSentiment/admin`
    and create a new user called `system`
  
 Note with the virtualenv setup, a symbolic link needs to be added so as to support the formatting
 with the new setup, something like that:
 
     ln -s /var/www/apps/finSentiment/env/lib/python3.4/site-packages/django/contrib/admin/static/admin /var/www/apps/finSentiment/twitterSentiment/static
 
 