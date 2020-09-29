from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search,name="search"),
    path('interface1',views.data,name="data"),
    path('interface2',views.interface2,name="interface2"),
    path('twitter/', views.results,name="twitter"),
    path('post/',views.display_tweets,name="post"),
    path('web/',views.web_data,name="web"),
    path('competitors/',views.competitor,name="comprtitors"),
    path('maps/',views.maps,name="map"),
    path('registration/',views.registration,name='register'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('mobilefetuers/',views.mobile_featuers,name='mobileFeatuers'),
    path('dataset/',views.data_set,name='dataset'),
    path('Apikeysumbit/',views.apikeysumbit , name='apiKeySumbit'),
]