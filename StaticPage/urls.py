from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home,name = "home"),
    path('privacy_policy/', views.Privacy, name="privacy"),
    path('term_of_services/', views.Services, name="services"),
]