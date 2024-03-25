from django.contrib import admin
from django.urls import include, path, re_path
from .views import search, manga_page, manga_page_count


app_name = 'manga'

api = [
    path('search/', search, name='search'),
    path('counts/<slug:slug>/', manga_page_count, name='counts')
]


urlpatterns = [
    path('api/', include(api)),
    path('manga/<slug:slug>/', manga_page, name='manga'),
]
