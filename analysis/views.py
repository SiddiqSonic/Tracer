# Create your views here.
import os
import pickle
from itertools import chain
from itertools import islice

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from Tracer import settings
#from analysis.WebScraper import GsmarenaScraper
#from analysis.sentimentTwitter import TwitterClient
from .form import CreateUserFrom
import urllib.request, json
from urllib.error import HTTPError
from .models import twitterAPIkey



@login_required(login_url='login')
def search(request):
    return render(request, 'analysis/search.html')


@login_required(login_url='login')
def data(request):
    try:
        if request.method == 'POST':
            key = request.POST['keyword']
            key = key.replace(" ", "_")
            competitor1 = request.POST['competitor1']
            competitor1 = competitor1.replace(" ", "_")
            competitor2 = request.POST['competitor2']
            competitor2 = competitor2.replace(" ", "_")
            competitor3 = request.POST['competitor3']
            competitor3 = competitor3.replace(" ", "_")
            dateSince = request.POST['dateSince']
            dateUntil = request.POST['dateUntil']
            print(dateSince)
            latitude = request.POST['latitude']
            longitute = request.POST['longitute']
            radius = ''

            count = request.POST['count']
            #count = int(count)
            # creating object of TwitterClient Class
            #api = TwitterClient()
            #gs = GsmarenaScraper()
            # calling function to get tweets

            positive_tweets_C1 = []
            negative_tweets_C1 = []
            neutral_tweets_C1 = []
            pcoordinates_C1 = []
            ncoordinates_C1 = []
            nucoordinates_C1 = []

            positive_tweets_C2 = []
            negative_tweets_C2 = []
            neutral_tweets_C2 = []
            pcoordinates_C2 = []
            ncoordinates_C2 = []
            nucoordinates_C2 = []

            positive_tweets_C3 = []
            negative_tweets_C3 = []
            neutral_tweets_C3 = []
            pcoordinates_C3 = []
            ncoordinates_C3 = []
            nucoordinates_C3 = []
            if latitude == "":
                latitude = "30"
            if longitute == "":
                longitute = "70"
            if radius == "":
                radius = "450"


            keys = twitterAPIkey.objects.last()
            if competitor1 != '':
                url = "http://127.0.0.1:8000/TwitterSentiments/?keyword="+competitor1+"&latitude="+latitude+"&longitude="+longitute+"&radius="+radius+"&count="+count+"&since_date="+dateSince+"&until_date="+dateUntil+"&consumer_key="+keys.Consumer_key+"&consumer_secret="+keys.Consumer_secret+"&access_token="+keys.Access_token+"&Access_token_secret="+keys.Access_token_secret
                response = {}
                with urllib.request.urlopen(url) as url:
                    response = json.loads(url.read().decode())



                positive_tweets_C1 = response["positive_text"]
                negative_tweets_C1 = response["Negative_text"]
                neutral_tweets_C1 = response["Neutral_text"]
                pcoordinates_C1 = response["pcoordinates"]
                ncoordinates_C1 = response["ncoordinates"]
                nucoordinates_C1 = response["nucoordinates"]


            if competitor2 != '':
                url = "http://127.0.0.1:8000/TwitterSentiments/?keyword=" + competitor2 + "&latitude=" + latitude + "&longitude=" + longitute + "&radius=" + radius + "&count=" + count + "&since_date=" + dateSince + "&until_date=" + dateUntil +"&consumer_key="+keys.Consumer_key+"&consumer_secret="+keys.Consumer_secret+"&access_token="+keys.Access_token+"&Access_token_secret="+keys.Access_token_secret
                response = {}
                with urllib.request.urlopen(url) as url:
                    response = json.loads(url.read().decode())


                positive_tweets_C2 = response["positive_text"]
                negative_tweets_C2 = response["Negative_text"]
                neutral_tweets_C2 = response["Neutral_text"]
                pcoordinates_C2 = response["pcoordinates"]
                ncoordinates_C2 = response["ncoordinates"]
                nucoordinates_C2 = response["nucoordinates"]





            if competitor3 != '':
                url = "http://127.0.0.1:8000/TwitterSentiments/?keyword=" + competitor3 + "&latitude=" + latitude + "&longitude=" + longitute + "&radius=" + radius + "&count=" + count + "&since_date=" + dateSince + "&until_date=" + dateUntil +"&consumer_key="+keys.Consumer_key+"&consumer_secret="+keys.Consumer_secret+"&access_token="+keys.Access_token+"&Access_token_secret="+keys.Access_token_secret
                response = {}

                with urllib.request.urlopen(url) as url:
                    response = json.loads(url.read().decode())


                positive_tweets_C3 = response["positive_text"]
                negative_tweets_C3 = response["Negative_text"]
                neutral_tweets_C3 = response["Neutral_text"]
                pcoordinates_C3 = response["pcoordinates"]
                ncoordinates_C3 = response["ncoordinates"]
                nucoordinates_C3 = response["nucoordinates"]



            url = "http://127.0.0.1:8000/TwitterSentiments/?keyword=" + key + "&latitude=" + latitude + "&longitude=" + longitute + "&radius=" + radius + "&count=" + count + "&since_date=" + dateSince + "&until_date=" + dateUntil +"&consumer_key="+keys.Consumer_key+"&consumer_secret="+keys.Consumer_secret+"&access_token="+keys.Access_token+"&Access_token_secret="+keys.Access_token_secret
            response = {}

            with urllib.request.urlopen(url) as url:
                response = json.loads(url.read().decode())


            tweet_id = response["tweets_id"]
            positive_tweets = response["positive_text"]
            negative_tweets = response["Negative_text"]
            neutral_tweets = response["Neutral_text"]
            count_positive = response["Positive_pre"]
            count_negative = response["Negative_Pre"]
            count_neutral = response["Neutral_Pre"]
            count_tweets = response["totaltweets"]
            wordcounts = response["wordcount"]
            male = response["male"]
            female = response["female"]
            pcoordinates = response["pcoordinates"]
            ncoordinates = response["ncoordinates"]
            nucoordinates = response["nucoordinates"]
            retweetcount = response["retweet"]

            if pcoordinates is None:
                pcoordinates = [30,70]
            if ncoordinates is None:
                ncoordinates = [30.458,70.12547]

            # After Prototype#


            response = {}

            url = "http://127.0.0.1:8000/ScraperSentiments/?keyword="+key+"&count="+count
            with urllib.request.urlopen(url) as url:
                response = json.loads(url.read().decode())

            count_positive_Scraper = response["positive_count_scraper"]
            count_negative_Scraper = response["negative_count_scraper"]
            count_neutral_Scraper = response["neutral_count_scraper"]
            count_review = response["total_review"]
            wordcounts_Scraper = response["wordcount_scraper"]
            positive_review = response["positive_review"]
            negative_review = response["negative_review"]
            neutral_review = response["neutral_review"]
            mobile_data = response["mobile_featuer"]

            results = {
                "tweets_id": tweet_id,
                "Positive_pre": count_positive,
                "Negative_Pre": count_negative,
                "Neutral_Pre": count_neutral,
                "retweet": retweetcount,
                "totaltweets": count_tweets,
                "wordcount": wordcounts,
                "male": male,
                "female": female,
                "Keyword": key.replace('_',' '),
                "positive_tweets":positive_tweets,
                "negative_tweets":negative_tweets,
                'neutral_tweets':neutral_tweets,

                "competitor1": competitor1,
                "competitor2": competitor2,
                "competitor3": competitor3,
                'postitive_count_C1': len(positive_tweets_C1),
                'negative_count_C1': len(negative_tweets_C1),
                'neutral_count_C1': len(neutral_tweets_C1),

                'postitive_count_C2': len(positive_tweets_C2),
                'negative_count_C2': len(negative_tweets_C2),
                'neutral_count_C2': len(neutral_tweets_C2),

                'postitive_count_C3': len(positive_tweets_C3),
                'negative_count_C3': len(negative_tweets_C3),
                'neutral_count_C3': len(neutral_tweets_C3),

                'pcoordinates': pcoordinates,
                'ncoordinates': ncoordinates,
                'pcoordinates_C1': pcoordinates_C1,
                'ncoordinates_C1': ncoordinates_C1,
                'pcoordinates_C2': pcoordinates_C2,
                'ncoordinates_C2': ncoordinates_C2,
                'pcoordinates_C3': pcoordinates_C3,
                'ncoordinates_C3': ncoordinates_C3,

                'total_review': count_review,
                'positive_count_scraper': count_positive_Scraper,
                'negative_count_scraper': count_negative_Scraper,
                'neutral_count_scraper': count_neutral_Scraper,
                'wordcounts_Scraper': wordcounts_Scraper,
                'positive_review' : positive_review,
                'negative_review': negative_review,
                'neutral_review' : neutral_review,

                'mobile_data' : mobile_data,
            }
            with open(os.path.join(settings.BASE_DIR, r'analysis\TempData.pickle'), 'wb') as f:
                pickle.dump(results, f)

            return render(request, "analysis/interfaces1.html", results)
        return HttpResponse("No data")
    except os.error as e:
        e = str(e)
        return HttpResponse("alert('"+e+"');")
    except HTTPError as e:
        e = str(e)
        return HttpResponse("alert('"+e+"');")
#    except :
#       return HttpResponse("alert('The expation is arised');")


@login_required(login_url='login')
def interface2(request):
    with open(os.path.join(settings.BASE_DIR, r'analysis\TempData.pickle'), 'rb') as f:
        result = pickle.load(f)
    return render(request, "analysis/interfaces2.html", result)



@login_required(login_url='login')
def results(request):
    with open(os.path.join(settings.BASE_DIR, r'analysis\TempData.pickle'), 'rb') as f:
        result = pickle.load(f)
    return render(request, "analysis/index.html", result)


@login_required(login_url='login')
def display_tweets(request):
    with open(os.path.join(settings.BASE_DIR, r'analysis\TempData.pickle'), 'rb') as f:
        result = pickle.load(f)
    return render(request, "analysis/tweets.html", result)


@login_required(login_url='login')
def maps(request):
    with open(os.path.join(settings.BASE_DIR, r'analysis\TempData.pickle'), 'rb') as f:
        result = pickle.load(f)
        return render(request, "analysis/maps.html", result)


@login_required(login_url='login')
def competitor(request):
    with open(os.path.join(settings.BASE_DIR, r'analysis\TempData.pickle'), 'rb') as f:
        result = pickle.load(f)
        return render(request, "analysis/competitor.html", result)

@login_required(login_url='login')
def web_data(request):
    with open(os.path.join(settings.BASE_DIR, r'analysis\TempData.pickle'), 'rb') as f:
        result = pickle.load(f)
        return render(request, "analysis/scraper.html", result)

def registration(request):
    form = CreateUserFrom()

    if request.method == 'POST':
        form = CreateUserFrom(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfuly')
            return redirect('login')
    results = {'form': form}
    return render(request, 'analysis/registration.html', results)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('search')
        else:
            messages.error(request, 'Username OR password is incorrect')
    return render(request, 'analysis/login.html')

def logout_request(request):
    logout(request)
    return render(request, 'analysis/login.html')

@login_required(login_url='login')
def mobile_featuers(request):
    with open(os.path.join(settings.BASE_DIR, r'analysis\TempData.pickle'), 'rb') as f:
        result = pickle.load(f)
    return  render(request,'analysis/mobileFeatuers.html', result)

@login_required(login_url='login')
def data_set(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request,'analysis/dataset.html')
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='login')
def data_setsumbit(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            return render(request,'analysis/dataset.html')
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='login')
def apikeysumbit(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            consumer_key = request.POST['consumer_key']
            consumer_secret = request.POST['consumer_secret']
            access_token = request.POST['Access_token']
            access_token_secret = request.POST['Access_token_secret']
            twitterkey = twitterAPIkey(Consumer_key=consumer_key,Consumer_secret = consumer_secret,Access_token=access_token,Access_token_secret=access_token_secret)
            twitterkey.save()
            return render(request,'analysis/dataset.html')
        return render(request, 'analysis/dataset.html')
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')