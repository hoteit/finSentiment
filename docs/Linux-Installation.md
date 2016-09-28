The application is mostly developed in Python using [Tweepy](http://www.tweepy.org) to extract tweets from Twitter, [Django](https://djangoproject.com) for the portal and to help train the machine learning algorithm, [Stanford Core NLP](https://stanfordnlp.github.io/CoreNLP) for the sentiment analysis, and various Python tools including [IPython](http://ipython.org/), [Pandas](http://pandas.pydata.org/), and [Django-extensions](https://github.com/django-extensions/django-extensions).

The requirements to setup the system is as follows. Note that it is assumed that we are installing on a Debian instance.

1) setup a Debian instance on a local machine, a Docker container, or a cloud instance. Then run:
     
     sudo apt-get update
     sudo apt-get upgrade

2) install python dev, mysql server and client
`sudo apt-get install mysql-server mysqlclient python-dev libmysqlclient-dev`
setup the root account and then run `sudo mysql_secure_installation`

3) make sure that Python3 is installed and install VirtualEnv so as to isolate our Python environment for the app only.
`sudo apt-get install virtualenv`

4) install apache2, and apache2 python modules

     sudo apt-get install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert libapache2-mod-wsgi

Now that you have the basic components installed, we will go ahead and setup the code, the code dependencies, and make the necessary configurations. Next: [[Django Setup]]

