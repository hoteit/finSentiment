I am assuming that you completed the steps under [[Linux Installation]]. Next is to setup the code.
1) Identify the location where you want the code to be setup. I will asssume that we will create it under /var/www/apps and with permissions correctly set. I personally have done the following
`sudo install -d -o tarek -g tarek /var/www/apps` (created the directory and updated the ownership for my settings)

Assuming that the directory is **/var/www/apps** and we are in that directory, `cd /var/www/apps`, let download the code.
2) `git clone https://github.com/hoteit/finSentiment`  (TODO: this will be replaced with some type of code packaging in the future)

3) Setup Python virtual environment and install the python requirements for the project Note: I am assuming your are in /var/www/apps/finSentiment

     virtualenv -p /usr/bin/python3 env
     source env/bin/activate
     (env) pip install -r requirements.txt

Note:  if you get specific errors when installing the requirements, check the [[errors]] page.

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
    
 b. activate the virtual directory `a2en
 c. update the file /var/www/apps/finSentiment/apache/wsgi.py with the location of your Python environment and the code
 d/ 


