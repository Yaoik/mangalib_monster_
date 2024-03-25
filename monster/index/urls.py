from django.contrib import admin
from django.urls import include, path, re_path
from .views import index, search_result


app_name = 'index'

urlpatterns = [
    path('', index, name='index'),
    path('search_result/', search_result, name='search_result'),
]
