from django.db import models
from manga.models import Manga
from annoying.fields import AutoOneToOneField



class MangaPage(models.Model):
    manga = AutoOneToOneField(Manga, primary_key=True, related_name='site_page', on_delete=models.CASCADE)

