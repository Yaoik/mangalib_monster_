from django.contrib import admin
from django.urls import include, path, re_path

api = [
    path('manga_page/', include('manga_page.urls')),
    path('manga/', include('manga.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api)),
]


