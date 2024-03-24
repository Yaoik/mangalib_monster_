from django.contrib import admin
from django.urls import include, path, re_path
from .views import index



app_name = 'index'

urlpatterns = [
    path('', index, name='index'),
]
