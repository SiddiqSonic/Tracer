from django.contrib.contenttypes import admin
from django.db import models
from django.contrib import admin

# Create your models here.

class twitterAPIkey(models.Model):
    Consumer_key = models.CharField(max_length=100)
    Consumer_secret = models.CharField(max_length=100)
    Access_token = models.CharField(max_length=100)
    Access_token_secret = models.CharField(max_length=100)

