from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest



def index(request:WSGIRequest):
    return render(request, 'index.html')


def search_result(request:WSGIRequest):
    return render(request, 'search_result.html')