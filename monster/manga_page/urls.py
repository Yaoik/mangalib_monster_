from django.contrib import admin
from django.urls import include, path, re_path
from .views import ListMangaPage, get_page, get_compressed

app_name = 'manga_page'

api = [
    path('manga_data/<slug:slug>/compressed', get_compressed, name='manga_data_compressed'),
]

urlpatterns = [
    path('list/', ListMangaPage.as_view(), name='manga_page_list'),
    path('api/', include(api)),
]
