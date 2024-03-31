from django.contrib import admin
from django.urls import include, path, re_path
from .views import search, manga_page, manga_page_count, add_stats, get_stats


app_name = 'manga'

api = [
    path('search/', search, name='search'),
    path('counts/<slug:slug>/', manga_page_count, name='counts'),
    path('add_stats/', add_stats, name='add_stats'),
    path('get_stats/', get_stats, name='get_stats'),
]


urlpatterns = [
    path('api/', include(api)),
    path('manga/<slug:slug>/', manga_page, name='manga'),
]
