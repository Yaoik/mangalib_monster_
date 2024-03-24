from django.contrib import admin
from django.urls import include, path, re_path

apps = [
    path('', include('manga_page.urls')),
    path('', include('manga.urls')),
    path('', include('index.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(apps)),
]


