"""
Project settings for finSentiment application.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '[CHANGE]'

DEBUG = True # change it when necessary

ALLOWED_HOSTS = []

PROJECT_ROOT = "[CHANGE]"
#update with the location of the finSentiment app eg. PROJECT_ROOT = "/apps/Documents/Projects/finSentiment"

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finsentimentdb', # insert database name
        'USER': 'financedbuser', # insert database user name
        'PASSWORD': '[CHANGE]', # insert database password
        'HOST': '',
        'PORT': '',
        'OPTIONS': {'charset': 'utf8mb4'},
        'CONN_MAX_AGE': None,
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'twitterSentiment',
    'django_extensions',
]

### IPython settings

IPYTHON_ARGUMENTS = [
            '--ext', 'django_extensions.management.notebook_extension',
             '--profile=phd', #customize based on your iPython profile
             '--debug'
]


#### Twitter Application settings - setup a Twitter app at https://apps.twitter.com
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

tweets_polling_time = 300 # in seconds, how long to wait till a new fresh of sampling is captured
tweets_polling_size = 200 # group of companies to monitor in each sampling
tweets_max_per_sample = 50 # maximum number of tweets detected per iteration


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'finSentiment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_ROOT+"/twitterSentiment/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'finSentiment.wsgi.application'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
  #  PROJECT_ROOT+'/scr/static',
)
STATIC_ROOT=PROJECT_ROOT+'/finSentiment/static'