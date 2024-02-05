from django.db import models
import re

class Tag(models.Model):    
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    href = models.CharField(max_length=255, unique=True)
    
    class Meta:
        verbose_name_plural = 'Тег'
        verbose_name = 'Тег'
    
    def __str__(self) -> str:
        return f'{self.name}'

class Team(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, null=False, unique=True)
    branch_id = models.PositiveSmallIntegerField()
    href = models.CharField(max_length=255, unique=True)
    img = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    alt_name = models.CharField(max_length=255, unique=True)
    cover = models.CharField(max_length=32)
    slug = models.CharField(max_length=255, unique=True)
    sale = models.PositiveSmallIntegerField()
    pivot = models.JSONField()
    
    class Meta:
        verbose_name_plural = 'Команда переводчиков'
        verbose_name = 'Команда переводчиков'
    
    def __str__(self) -> str:
        return f'{self.name}'
    
class Chapter(models.Model):
    chapter_id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    chapter_slug = models.CharField(null=False, unique=True, max_length=255)
    chapter_name = models.CharField(max_length=255)
    chapter_number = models.CharField(max_length=12)
    chapter_volume = models.PositiveSmallIntegerField()
    chapter_moderated = models.PositiveSmallIntegerField()
    chapter_user_id = models.PositiveIntegerField()
    chapter_expired_at = models.CharField(max_length=20)
    chapter_created_at = models.CharField(max_length=20)
    chapter_scanlator_id = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=255, null=True)
    price = models.PositiveIntegerField()
    branch_id = models.PositiveIntegerField()
    username = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = 'Глава'
        verbose_name = 'Глава'
    
    def __str__(self) -> str:
        return f'{self.chapter_name}'
    
class Manga(models.Model):
    img = models.CharField(max_length=255, unique=True, null=False)
    href = models.CharField(max_length=255, unique=True, null=False)
    tags = models.ManyToManyField(Tag)
    description = models.TextField(unique=True, null=False)
    type = models.CharField(max_length=32, null=False)
    release_year = models.PositiveSmallIntegerField(null=False)
    title_status = models.CharField(max_length=32, null=False)
    transfer_status = models.CharField(max_length=32, null=False)
    author = models.CharField(max_length=255, null=False)
    artist = models.CharField(max_length=255, null=False)
    publishing_house = models.CharField(max_length=255, null=False)
    age_rating = models.CharField(max_length=3, null=False)
    chapters_uploaded = models.PositiveSmallIntegerField(null=False)
    alternative_names = models.JSONField(unique=True, null=True)
    teams = models.ManyToManyField(Team)
    rus_name = models.CharField(max_length=255, unique=True, null=False)
    eng_name = models.CharField(max_length=255, unique=True, null=False)
    slug = models.CharField(max_length=255, unique=True, null=False)
    status = models.PositiveSmallIntegerField(null=False)
    chapters = models.ManyToManyField(Chapter)
    in_lists = models.JSONField(null=True)
    rating = models.FloatField(null=True)
    number_of_ratings = models.PositiveIntegerField(null=True)
    scores = models.JSONField(null=True)
    related = models.JSONField(null=True)
    similar = models.JSONField(null=True) 
    
    class Meta:
        verbose_name_plural = 'Манга'
        verbose_name = 'Манга'
    
    def __str__(self):
        return f'{self.rus_name}'