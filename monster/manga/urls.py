from django.contrib import admin
from django.urls import include, path, re_path
from .views import search


app_name = 'manga'

urlpatterns = [
    path('search/', search, name='manga_list'),
]
