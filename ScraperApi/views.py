# Create your views here.
import operator
import collections

from rest_framework.views import APIView
from ScraperApi.WebScraper import GsmarenaScraper
from itertools import chain, islice
from rest_framework.response import Response
from collections import OrderedDict


class ScraperSentiments(APIView):
    def get(self, request):

        keyword = self.request.query_params.get('keyword')
        count = self.request.query_params.get('count')

        gs = GsmarenaScraper()
        # After Prototype
        positive_review = []
        negative_review = []
        neutral_review = []
        text = []
        # calling the method of WebScraper.py
        reviews ,mob_data = gs.scraper(phone_name=keyword, count=count)
        for review in reviews:
            if review['sentiment'] == 'positive':
                positive_review.append(review["text"])
            elif review['sentiment'] == 'negative':
                negative_review.append(review["text"])
            elif review['sentiment'] == 'neutral':
                neutral_review.append(review["text"])
            text.append(review['clean_text'])

        count_positive_scraper = len(positive_review)
        count_negative_scraper = len(negative_review)
        count_neutral_scraper = len(neutral_review)
        count_review = len(reviews)

        words = []
        for sentence in text:
            words.append(sentence.split())
        words = list(chain.from_iterable(words))
        wordcount_scraper = gs.wordcount(words)
        #wordcount_scraper = sorted(wordcount_scraper.items(), key=lambda x: x[1])
        wordcount_scraper = dict(islice(wordcount_scraper.items(), 20))

        data = {
            'total_review': count_review,
            'positive_review': positive_review,
            'negative_review': negative_review,
            'neutral_review' : neutral_review,
            'positive_count_scraper': count_positive_scraper,
            'negative_count_scraper': count_negative_scraper,
            'neutral_count_scraper': count_neutral_scraper,
            'wordcount_scraper': wordcount_scraper,
            'mobile_featuer' : mob_data,
        }
        return Response(data)
