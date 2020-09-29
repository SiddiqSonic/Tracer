from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def Home(request):
    return render(request,'StaticPage/index.html')

def Privacy(request):
    return render(request,'StaticPage/privacy.html')

def Services(request):
    return render(request,'StaticPage/service.html')
