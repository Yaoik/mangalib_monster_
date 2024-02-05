from django.contrib import admin
from manga.models import AgeRestriction, MangaType, Moderated, Team, Genre, Tag, Publisher, People, MangaStatus, ScanlateStatus, Manga

admin.site.register(AgeRestriction)
admin.site.register(MangaType)
admin.site.register(Moderated)
admin.site.register(Team)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Publisher)
admin.site.register(People)
admin.site.register(MangaStatus)
admin.site.register(ScanlateStatus)
admin.site.register(Manga)

