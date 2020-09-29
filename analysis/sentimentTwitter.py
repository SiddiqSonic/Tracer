import datetime
import os
import re
import tweepy
from tweepy import OAuthHandler
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle
from django.conf import settings
from analysis.Naive import GenderAlgo
from itertools import islice
import geocoder
from textblob import TextBlob

stop_words = set(stopwords.words('english'))

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\classifier.pickle'), 'rb') as f:
    clf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\tfidfVectorizerModel.pickle'), 'rb') as f:
    tfidf = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, r'analysis\Naive\GenderClf.pickle'), 'rb') as f:
    Gclf = pickle.load(f)


class TwitterClient(object):

    def __init__(self):
        consumer_key = 'w9G7yqJXhkfhaBRlLhnSHMQET'
        consumer_secret = 'trrSp2hJefDzcTdgsQv4DNhuZR8tGyj8fQJF5m2juBLHygfJsi'
        access_token = '85805130-AK7uXWpTbtXJ9CqKWv584tH7iUQcBcNyhtm0mLM5U'
        access_token_secret = 'zWF6ASX4WIOfFieyG45xfaHEYrPujg7U1VGDqPLKxv3R5'
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def get_tweets(self, query,lat,log,radius,since,until,count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
        if since != '':
            since = datetime.datetime.strptime(since, "%Y-%m-%d")
            since = '{0}-{1}-{2}'.format(since.year,since.month,since.day)
        if until != '':
            until = datetime.datetime.strptime(until, "%Y-%m-%d")
            until = '{0}-{1}-{2}'.format( until.year,until.month,until.day)
        try:
            # call twitter api to fetch tweets
            geo = "" + lat + "," + log + "," + radius + "mi"
            #fetched_tweets = self.api.search(q=query,geocode=geo,count=count)
            fetched_tweets = tweepy.Cursor(self.api.search, q=query,lang='en',since=since,until=until,geo=geo).items(count)

            # parsing tweets one by one

            for tweet in fetched_tweets:

                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                parsed_tweet['id'] = tweet.id
                parsed_tweet['location'] = tweet.user.location

                parsed_tweet['retweetcount'] = tweet.retweet_count
                parsed_tweet['gender'] = Gclf.classify(GenderAlgo.gender_features(tweet.user.name))
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                parsed_tweet['coordinates'] = tweet.coordinates

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


    def get_tweet_sentiment(self, tweet=[]):
        tweet = ' '.join(self.clean_tweet(tweet))
        ls = [tweet]
        tweet=tfidf.transform(ls).toarray()
        return clf.predict(tweet)



    def clean_tweet(self, tweet):
        text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', ' ', tweet)
        text = re.sub(r'@[A-Za-z0-9_]+', ' ', text)
        text = text.lower()
        text = re.sub(r"RT", " ", text)
        text = re.sub(r"that's", "that is", text)
        text = re.sub(r"there's", "there is", text)
        text = re.sub(r"what's", "what is", text)
        text = re.sub(r"where's", "where is", text)
        text = re.sub(r"it's", "it is", text)
        text = re.sub(r"who's", "who is", text)
        text = re.sub(r"i'm", "i am", text)
        text = re.sub(r"she's", "she is", text)
        text = re.sub(r"he's", "he is", text)
        text = re.sub(r"they're", "they are", text)
        text = re.sub(r"who're", "who are", text)
        text = re.sub(r"ain't", "am not", text)
        text = re.sub(r"wouldn't", "would not", text)
        text = re.sub(r"shouldn't", "should not", text)
        text = re.sub(r"couldn't", "could not", text)
        text = re.sub(r"can't", "can not", text)
        text = re.sub(r"won't", "will not", text)
        text = re.sub(r'@[^\s]+', ' ', text)
        text = re.sub(r"\W", " ", text)
        text = re.sub(r"\d", " ", text)
        text = re.sub(r"^\s", " ", text)
        text = re.sub(' +', ' ', text)
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        return filtered_sentence


    def wordcount(self, tweet=[]):

        counts = dict()
        for word in tweet:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        return counts



    def take(n, iterable):
        "Return first n items of the iterable as a list"
        return list(islice(iterable, n))