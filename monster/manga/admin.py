from django.contrib import admin
from manga.models import Tag, Manga, Team, Chapter

admin.site.register(Tag)
admin.site.register(Manga)
admin.site.register(Team)
admin.site.register(Chapter)
