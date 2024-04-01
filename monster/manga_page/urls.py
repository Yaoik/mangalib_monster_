from django.contrib import admin
from django.urls import include, path, re_path
from .views import ListMangaPage, get_page, get_population_compressed, get_toxic_compressed, get_at_days, get_at_days_percent, get_24

app_name = 'manga_page'

api = [
    path('manga_data/<slug:slug>/compressed', get_population_compressed, name='manga_data_population_compressed'),
    path('manga_data/<slug:slug>/toxic', get_toxic_compressed, name='manga_data_toxic_compressed'),
    path('manga_data/<slug:slug>/at_days', get_at_days, name='manga_data_at_days'),
    path('manga_data/<slug:slug>/at_days_percent', get_at_days_percent, name='manga_data_at_days_percent'),
    path('manga_data/<slug:slug>/at_24_h', get_24, name='manga_data_24'),
    path('manga_data/<slug:slug>/', get_page, name='manga_data'),
]

urlpatterns = [
    path('list/', ListMangaPage.as_view(), name='manga_page_list'),
    path('api/', include(api)),
]
