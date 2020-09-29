from itertools import chain, islice
#http://127.0.0.1:8000/TwitterSentiments/?keyword=Nokia&latitude=30&longitude=70&radius=450&count=10&since_date=2020-9-22&until_date=2020-9-29&consumer_key=w9G7yqJXhkfhaBRlLhnSHMQET&consumer_secret=trrSp2hJefDzcTdgsQv4DNhuZR8tGyj8fQJF5m2juBLHygfJsi&access_token=85805130-AK7uXWpTbtXJ9CqKWv584tH7iUQcBcNyhtm0mLM5U&Access_token_secret=zWF6ASX4WIOfFieyG45xfaHEYrPujg7U1VGDqPLKxv3R5
from django.shortcuts import render
# http://127.0.0.1:8000/TwitterSentiments/?keyword=Nokia&latitude=30&longitude=70&radius=450&count=10&since_date=2020-4-9&until_date=2020-4-11
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from twitterapi.sentimentTwitter import TwitterClient


class TwitterSentiments(APIView):
    def get(self, request):

        keyword = self.request.query_params.get('keyword')
        count = self.request.query_params.get('count')
        since_date = self.request.query_params.get('since_date')
        until_date = self.request.query_params.get('until_date')
        lat = self.request.query_params.get('latitude')
        lng = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius')
        Consumer_key =self.request.query_params.get('consumer_key')
        Consumer_secret =self.request.query_params.get('consumer_secret')
        Access_token =self.request.query_params.get('access_token')
        Access_token_secret = self.request.query_params.get('Access_token_secret')
        if Consumer_key is None:
            Consumer_key = 'w9G7yqJXhkfhaBRlLhnSHMQET'
        if Consumer_secret is None:
            Consumer_secret = 'trrSp2hJefDzcTdgsQv4DNhuZR8tGyj8fQJF5m2juBLHygfJsi'
        if Access_token is None:
            Access_token = '85805130-AK7uXWpTbtXJ9CqKWv584tH7iUQcBcNyhtm0mLM5U'
        if Access_token_secret is None:
            Access_token_secret = 'zWF6ASX4WIOfFieyG45xfaHEYrPujg7U1VGDqPLKxv3R5'

        api = TwitterClient(Consumer_key=Consumer_key,Consumer_secret=Consumer_secret,Access_token=Access_token, Access_token_secret = Access_token_secret)
        positive_tweets = []
        negative_tweets = []
        neutral_tweets = []
        male = []
        female = []
        text = []
        tweet_id = []
        pcoordinates = []
        ncoordinates = []
        nucoordinates = []
        retweetcount = 0

        tweets = api.get_tweets(query=keyword, lat=lat, log=lng, since=since_date, until=until_date, radius=radius,
                                count=count)

        for tweet in tweets:

            retweetcount = retweetcount + tweet['retweetcount']
            text.append(api.clean_tweet(tweet['text']))
            tweet_id.append(tweet['id'])

            if tweet['sentiment'] == 'positive':
                positive_tweets.append(tweet['text'])
                pcoordinates.append(tweet['coordinates'])
            elif tweet['sentiment'] == 'negative':
                negative_tweets.append(tweet['text'])
                ncoordinates.append(tweet['coordinates'])
            elif tweet['sentiment'] == 'neutral':
                neutral_tweets.append(tweet['text'])
                nucoordinates.append(tweet['coordinates'])
            if tweet['gender'] == 'male':
                male.append(tweet)
            elif tweet['gender'] == 'female':
                female.append(tweet)

        count_positive = len(positive_tweets)
        count_negative = len(negative_tweets)
        count_neutral = len(neutral_tweets)
        count_tweets = len(tweets)

        text = list(chain.from_iterable(text))
        wordcounts = api.wordcount(text)
        wordcounts = dict(islice(wordcounts.items(), 20))

        data = {
            "tweets_id": tweet_id,
            "Positive_pre": count_positive,
            "Negative_Pre": count_negative,
            "Neutral_Pre": count_neutral,
            "retweet": retweetcount,
            "totaltweets": count_tweets,
            "wordcount": wordcounts,
            "male": len(male),
            "female": len(female),
            'pcoordinates': pcoordinates,
            'nucoordinates': nucoordinates,
            'ncoordinates': ncoordinates,
            "positive_text": positive_tweets,
            "Neutral_text": neutral_tweets,
            "Negative_text": negative_tweets,
            "Keyword": keyword,

        }
        return Response(data)
