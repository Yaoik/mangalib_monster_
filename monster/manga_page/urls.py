from django.contrib import admin
from django.urls import include, path, re_path
from .views import ListMangaPage

app_name = 'manga_page'

urlpatterns = [
    path('list/', ListMangaPage.as_view(), name='manga_page_list'),
]
