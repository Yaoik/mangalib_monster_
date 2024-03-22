from django.contrib import admin
from django.urls import include, path, re_path

api = [
    path('manga/', include('manga_page.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api)),
]


