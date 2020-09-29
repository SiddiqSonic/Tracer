from django.urls import path
from . import views

urlpatterns = [
    path('ScraperSentiments/', views.ScraperSentiments.as_view(), name="scraper"),
]
