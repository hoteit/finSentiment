__author__ = 'tarek'

from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from twitterSentiment import views

urlpatterns = [url(r'^tweet_count/$', views.requires_login(views.GetTweetStats),name="streamStats"),\
                       url(r'^trainingDS/$', views.requires_login(views.pick_trainingDatum), name='trainingDS'),
                       url(r'^$', views.requires_login(views.index), name='index'),\
                       url(r'^login/$', views.login_user, name='login'),\
                       url(r'^logout/$', views.logout_user, name='logout')]


