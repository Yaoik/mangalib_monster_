from django.db import models
import re

class AgeRestriction(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, unique=True)
    label = models.CharField(max_length=8, unique=True)
    
    class Meta:
        verbose_name_plural = 'Возрастное ограничение'
        verbose_name = 'Возрастное ограничение'

    def __str__(self):
        return f'{self.label}'
    
class MangaType(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, unique=True)
    label = models.CharField(max_length=32, unique=True)
    
    class Meta:
        verbose_name_plural = 'Тип произведения'
        verbose_name = 'Тип произведения'

    def __str__(self):
        return f'{self.label}'

class Moderated(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, unique=True)
    label = models.CharField(max_length=32, unique=True)
    
    class Meta:
        verbose_name_plural = 'Статус модерации'
        verbose_name = 'Статус модерации'

    def __str__(self):
        return f'{self.label}'

class Team(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    slug_url = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    cover = models.JSONField()
    details = models.JSONField()
    
    class Meta:
        verbose_name_plural = 'Переводчики'
        verbose_name = 'Переводчики'

    def __str__(self):
        return f'{self.name}'
    
class Genre(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=64, unique=True)
    
    class Meta:
        verbose_name_plural = 'Жанр'
        verbose_name = 'Жанр'

    def __str__(self):
        return f'{self.name}'

class Tag(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=64, unique=True)
    
    class Meta:
        verbose_name_plural = 'Тег'
        verbose_name = 'Тег'

    def __str__(self):
        return f'{self.name}'
    
class Publisher(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    slug_url = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    rus_name = models.CharField(max_length=255, unique=True, null=True)
    cover = models.JSONField(null=True)
    subscription = models.JSONField(null=True)
    
    class Meta:
        verbose_name_plural = 'Издатель'
        verbose_name = 'Издатель'

    def __str__(self):
        return f'{self.name}'
    
class People(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    slug_url = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    rus_name = models.CharField(max_length=255, unique=True, null=True)
    alt_name = models.CharField(max_length=255, unique=True, null=True)
    cover = models.JSONField(null=True)
    subscription = models.JSONField(null=True)
    user_id = models.SmallIntegerField()
    titles_count_details = models.CharField(max_length=255, null=True)
    
    class Meta:
        verbose_name_plural = 'Автор'
        verbose_name = 'Автор'

    def __str__(self):
        return f'{self.name}'
    
class MangaStatus(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, unique=True)
    label = models.CharField(max_length=32, unique=True)
    
    class Meta:
        verbose_name_plural = 'Статус выпуска манги'
        verbose_name = 'Статус выпуска манги'

    def __str__(self):
        return f'{self.label}'
    
class ScanlateStatus(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, unique=True)
    label = models.CharField(max_length=32, unique=True)
    
    class Meta:
        verbose_name_plural = 'Статус выпуска перевода'
        verbose_name = 'Статус выпуска перевода'

    def __str__(self):
        return f'{self.label}'
    
class Manga(models.Model):
    id = models.SmallIntegerField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=255)
    rus_name = models.CharField(max_length=255)
    eng_name = models.CharField(max_length=255)
    otherNames = models.JSONField()
    slug = models.CharField(max_length=255)
    slug_url = models.CharField(max_length=255)
    cover = models.JSONField()
    background = models.JSONField()
    age_restriction = models.ForeignKey(AgeRestriction, on_delete=models.SET_NULL, null=True)
    site = models.SmallIntegerField()
    type = models.ForeignKey(MangaType, on_delete=models.SET_NULL, null=True)
    summary = models.TextField()
    close_view = models.SmallIntegerField()
    releaseDate = models.SmallIntegerField()
    views = models.JSONField()
    rating = models.JSONField()
    is_licensed = models.BooleanField()
    moderated = models.ForeignKey(Moderated, on_delete=models.SET_NULL, null=True)
    teams = models.ManyToManyField(Team)
    genres = models.ManyToManyField(Genre)
    tags = models.ManyToManyField(Tag)
    publisher = models.ManyToManyField(Publisher)
    metadata = models.JSONField()
    model = models.CharField(max_length=255)
    status = models.ManyToManyField(MangaStatus)
    items_count = models.JSONField()
    scanlate_status = models.ManyToManyField(ScanlateStatus)
    format = models.JSONField()
    release_date_string = models.CharField(max_length=16)

    artists = models.ManyToManyField(People, related_name='artist_manga_set')
    authors = models.ManyToManyField(People, related_name='author_manga_set')
    
    class Meta:
        verbose_name_plural = 'Манга'
        verbose_name = 'Манга'

    def __str__(self):
        return f'{self.name}'