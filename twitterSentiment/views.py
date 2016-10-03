from django.shortcuts import render
from django.views import generic
from django import forms
from twitterSentiment.models import Company, TwitterText, CompanySentiment
from twitterSentiment.forms import CompaniesImport, TrainingDatumForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.core import urlresolvers
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.template import RequestContext
import random


def requires_login(view):
    def protected_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(urlresolvers.reverse('login'))
        return view(request, *args, **kwargs)

    return protected_view


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(urlresolvers.reverse('login'))


def not_authorized(request):
    logout(request)
    return HttpResponseRedirect('/twitterSentiment/notauthorized.html')  # TODO: make sure to have a template


def login_user(request):
    auth_message = "Please log in below "
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                auth_message = "You're successfully logged in."
                return HttpResponseRedirect(urlresolvers.reverse('index'))
            else:
                auth_message = "Your account is not active. Please contact your administrator."
        else:
            auth_message = "Your username and/or password is incorrect. Please try again."
    context = {'auth_message': auth_message, 'username': username}
    return render(request, 'twitterSentiment/login.html', context)


def GetTweetStats(request):
    total_tweets = TwitterText.objects
    tweet_count = total_tweets.count()
    untrained_count = total_tweets.filter(twitter_for_training="9").count()
    classified_count = CompanySentiment.objects.count()
    ready_to_train_count = total_tweets.filter(twitter_for_training="2").count()
    return render(request, 'twitterSentiment/tweet_count.html',
                  {'tweet_count': tweet_count, 'untrained_count': untrained_count,
                   'classified_count': classified_count, 'ready_to_train_count': ready_to_train_count},
                  )


class IndexView(generic.ListView):
    """ main page that shows the list of companies
    """
    context_object_name = "all_companies"
    model = Company

    def get_queryset(self):
        """
        :returns list of all the companies
        """
        return Company.objects.filter()

    template_name = "twitterSentiment/company_list.html"


class Company_New(generic.CreateView):
    model = Company
    template_name = "twitterSentiment/company_new.html"


def get_companies(request):
    """
    :param request: input a delimited list of companies
    :return: a list of companies
    """
    if request.method == 'POST':
        form = CompaniesImport(request.POST)
        if form.is_valid():
            companies_list = form['companies_list'].as_text().split(';')
            return HttpResponseRedirect('/thanks/')
    else:  # form is GET
        form = CompaniesImport()

    return render(request, 'twitterSentiment/companiesimporter.html', {'form': form})


def pick_trainingDatum(request):
    """
    the purpose of this function is pick a Twitter training message in order to be classified
    between 0 and 4 for sentiment
    :param request:
    :return:
    """

    if request.method == 'POST':
        form = TrainingDatumForm(request.POST)
        if form.is_valid():
            tweet = TwitterText.objects.get(id=request.POST['tweet_id'])
            tweet.twitter_for_training = "0"
            tweet.training_user = request.user
            tweet.twitter_sentiment = form.cleaned_data['twitter_sentiment']
            tweet.save()
            return HttpResponseRedirect(reverse_lazy('trainingDS'))
        return render(request, 'twitterSentiment/trainingds.html',
                      {'form': form})
    else:
        get_untrained_sentiments = TwitterText.objects.filter(twitter_for_training="9")
        num_untrained_sentiments = get_untrained_sentiments.count()
        # pick a tweet randomly

        if num_untrained_sentiments > 0:
            atweet_rnd_loc = random.randint(0, num_untrained_sentiments - 1)
            pick_object = get_untrained_sentiments[atweet_rnd_loc]
            tweet_id = pick_object.id
            form = TrainingDatumForm(instance=pick_object,
                                     initial={'twitter_for_training': "0", 'training_user': request.user})
            # note twitter_for_training = 0 means the tweet is being trained
            return render(request, 'twitterSentiment/trainingds.html',
                          {'form': form, 'tweet_id': tweet_id, 'message': pick_object.twitter_text})

        else:
            return render(request, 'twitterSentiment/done.html')


def index(request):
    return render(request, "twitterSentiment/index.html")
