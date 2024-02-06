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
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
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
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    slug_url = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    rus_name = models.CharField(max_length=255, unique=True, null=True)
    alt_name = models.CharField(max_length=255, unique=True, null=True)
    cover = models.JSONField(null=True)
    confirmed = models.CharField(max_length=255, null=True)
    subscription = models.JSONField(null=True)
    user_id = models.PositiveIntegerField()
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
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=255)
    rus_name = models.CharField(max_length=255)
    eng_name = models.CharField(max_length=255)
    other_names = models.JSONField()
    slug = models.CharField(max_length=255)
    slug_url = models.CharField(max_length=255)
    cover = models.JSONField()
    background = models.JSONField()
    age_restriction = models.ForeignKey(AgeRestriction, on_delete=models.SET_NULL, null=True)
    site = models.PositiveSmallIntegerField()
    type = models.ForeignKey(MangaType, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(null=True)
    close_view = models.PositiveSmallIntegerField()
    release_date = models.PositiveSmallIntegerField()
    views = models.JSONField()
    rating = models.JSONField()
    is_licensed = models.BooleanField()
    moderated = models.ForeignKey(Moderated, on_delete=models.SET_NULL, null=True)
    teams = models.ManyToManyField(Team)
    genres = models.ManyToManyField(Genre)
    tags = models.ManyToManyField(Tag)
    publishers = models.ManyToManyField(Publisher)
    metadata = models.JSONField()
    model = models.CharField(max_length=255)
    status = models.ForeignKey(MangaStatus, on_delete=models.SET_NULL, null=True)
    items_count = models.JSONField()
    scanlate_status = models.ForeignKey(ScanlateStatus, on_delete=models.SET_NULL, null=True)
    format = models.JSONField()
    release_date_string = models.CharField(max_length=16)
    artists = models.ManyToManyField(People, related_name='artist_manga_set')
    authors = models.ManyToManyField(People, related_name='author_manga_set')
    
    class Meta:
        verbose_name_plural = 'Манга'
        verbose_name = 'Манга'

    def __str__(self):
        return f'{self.name}'
    
    @property
    def href(self):
        return f'https://test-front.mangalib.me/ru/manga/{self.slug}'

class MangaUser(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    username = models.CharField(max_length=255, null=False, unique=True)
    avatar = models.JSONField(null=True, default=None)
    class Meta:
        verbose_name_plural = 'Пользователь'
        verbose_name = 'Пользователь'

    def __str__(self):
        return f'{self.username}'
    
class Branch(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    branch_id = models.PositiveIntegerField(null=False)
    created_at = models.DateTimeField(null=False)
    teams = models.ManyToManyField(Team)
    user = models.ForeignKey(MangaUser, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Ветка'
        verbose_name = 'Ветка'

    def __str__(self):
        return f'Ветка №{self.id}'
    
class Page(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    image = models.CharField(max_length=255, null=True)
    slug = models.PositiveSmallIntegerField(null=False)
    external = models.PositiveSmallIntegerField(null=False)
    chunks = models.PositiveSmallIntegerField(null=False)
    chapter_id = models.PositiveIntegerField(null=False, unique=True)
    created_at = models.DateTimeField(null=False)
    updated_at = models.DateTimeField(null=False)
    height = models.PositiveSmallIntegerField(null=False)
    width = models.PositiveSmallIntegerField(null=False)
    url = models.CharField(max_length=255, null=True)
    
    class Meta:
        verbose_name_plural = 'Страница'
        verbose_name = 'Страница'

    def __str__(self):
        return f'{self.url}'

class Chapter(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    manga_id = models.ForeignKey(Manga, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
    created_at = models.DateTimeField(null=True)
    moderated = models.ForeignKey(Moderated, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=32, null=True)
    index = models.PositiveSmallIntegerField(null=False)
    item_number = models.PositiveSmallIntegerField(null=False)
    volume = models.CharField(max_length=32, null=False)
    number = models.CharField(max_length=32, null=False)
    number_secondary = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=255, null=False)
    slug = models.CharField(max_length=255, null=True)
    branches_count = models.PositiveSmallIntegerField(null=False)
    
    class Meta:
        verbose_name_plural = 'Глава'
        verbose_name = 'Глава'

    def __str__(self):
        return f'{self.name}'

class Comment(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    comment = models.TextField(null=False)
    created_at = models.DateTimeField(null=False)
    comment_level = models.PositiveSmallIntegerField(null=False)
    parent_comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, related_name='parent_comment_foreigth_key')
    root_id = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, related_name='root_comment_foreigth_key')
    post_page = models.ForeignKey(Page, on_delete=models.CASCADE)
    user = models.ForeignKey(MangaUser, on_delete=models.CASCADE)
    votes_up = models.PositiveIntegerField(null=False)
    votes_down = models.PositiveIntegerField(null=False)
    relation_type = models.CharField(max_length=255)
    relation_id = models.PositiveIntegerField(null=False)
    
    class Meta:
        verbose_name_plural = 'Глава'
        verbose_name = 'Глава'

    def __str__(self):
        return f'Комментарий {str(self.user)}'






















































































































