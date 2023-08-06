from django.shortcuts import render
from django.template import loader

def index(request):
    context = {"Hello": "Hello Warise!!"}
    return render(request, "greeting/index.html", context)
