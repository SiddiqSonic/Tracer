from django.test import TestCase

# Create your tests here.
# -*- coding: utf-8 -*-
import urllib.request, json
dic = {}

with urllib.request.urlopen("http://127.0.0.1:8000/ScraperSentiments/?keyword=Nokia&count=10") as url:
    dic = json.loads(url.read().decode())


print(dic)