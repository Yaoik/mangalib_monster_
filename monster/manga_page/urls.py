from django.contrib import admin
from django.urls import include, path, re_path
from .views import ListMangaPage, get_page, get_population_compressed, get_toxic_compressed

app_name = 'manga_page'

api = [
    path('manga_data/<slug:slug>/compressed', get_population_compressed, name='manga_data_population_compressed'),
    path('manga_data/<slug:slug>/toxic', get_toxic_compressed, name='manga_data_toxic_compressed'),
    path('manga_data/<slug:slug>/', get_page, name='manga_data'),
]

urlpatterns = [
    path('list/', ListMangaPage.as_view(), name='manga_page_list'),
    path('api/', include(api)),
]
