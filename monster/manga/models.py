import logging
import random
from django.db import models
import re
from django.db.models import Q, Max, Min, Avg, Sum
from django.core.validators import MaxValueValidator, MinValueValidator
from asgiref.sync import sync_to_async
from annoying.fields import AutoOneToOneField
from django.db.models.query import QuerySet
from icecream import ic
from django.db.models.fields.json import KT
from django.db.models import IntegerField, FloatField
from django.db.models.functions import Cast
import time


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
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True) # id
    slug = models.CharField(max_length=255) # slug
    slug_url = models.CharField(max_length=255, unique=True) # slug_url
    name = models.CharField(max_length=255) # name
    cover = models.JSONField() # cover
    details = models.JSONField(null=True)
    model = models.CharField(max_length=10, null=True)
    vk = models.CharField(max_length=255, null=True) 
    discord = models.CharField(max_length=255, null=True) 

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
    slug = models.CharField(max_length=255)
    slug_url = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    rus_name = models.CharField(max_length=255, null=True)
    cover = models.JSONField(null=True)
    subscription = models.JSONField(null=True)
    
    class Meta:
        verbose_name_plural = 'Издатель'
        verbose_name = 'Издатель'

    def __str__(self):
        return f'{self.name}'
    
class People(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    slug = models.CharField(max_length=255)
    slug_url = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    rus_name = models.CharField(max_length=255, null=True)
    alt_name = models.CharField(max_length=255, null=True)
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
    
    meta_data = None
    
    @classmethod
    def make_json(cls):
        start = time.time()
        stats = Stats.objects.filter(Q(rating__isnull=False) & Q(bookmarks__isnull=False))

        if cls.meta_data is not None:
            if cls.meta_data.get('len(stats)') == len(stats):
                return cls.meta_data

        res = stats.annotate(
            bookmarks_count=Cast(KT('bookmarks__count'), IntegerField()), # type: ignore
            bookmarks_read_percent=Cast(KT('bookmarks__stats__0__percent'), FloatField()), # type: ignore
            bookmarks_in_plan_percent=Cast(KT('bookmarks__stats__1__percent'), FloatField()), # type: ignore
            bookmarks_drop_percent=Cast(KT('bookmarks__stats__2__percent'), FloatField()), # type: ignore
            bookmarks_readed_percent=Cast(KT('bookmarks__stats__3__percent'), FloatField()), # type: ignore
            bookmarks_favorite_percent=Cast(KT('bookmarks__stats__4__percent'), FloatField()), # type: ignore
            bookmarks_another_percent=Cast(KT('bookmarks__stats__5__percent'), FloatField()), # type: ignore
            
            rating_count=Cast(KT('rating__count'), IntegerField()), # type: ignore
            rating_10_percent=Cast(KT('rating__stats__0__percent'), FloatField()), # type: ignore 
            rating_9_percent=Cast(KT('rating__stats__1__percent'), FloatField()), # type: ignore 
            rating_8_percent=Cast(KT('rating__stats__2__percent'), FloatField()), # type: ignore 
            rating_7_percent=Cast(KT('rating__stats__3__percent'), FloatField()), # type: ignore 
            rating_6_percent=Cast(KT('rating__stats__4__percent'), FloatField()), # type: ignore 
            rating_5_percent=Cast(KT('rating__stats__5__percent'), FloatField()), # type: ignore 
            rating_4_percent=Cast(KT('rating__stats__6__percent'), FloatField()), # type: ignore 
            rating_3_percent=Cast(KT('rating__stats__7__percent'), FloatField()), # type: ignore 
            rating_2_percent=Cast(KT('rating__stats__8__percent'), FloatField()), # type: ignore 
            rating_1_percent=Cast(KT('rating__stats__9__percent'), FloatField()), # type: ignore
        )
        
        bookmarks = res.aggregate(
            bookmarks_count_avg=Avg('bookmarks_count'),
            bookmarks_read_percent_avg=Avg('bookmarks_read_percent'),
            bookmarks_in_plan_percent_avg=Avg('bookmarks_in_plan_percent'),
            bookmarks_drop_percent_avg=Avg('bookmarks_drop_percent'),
            bookmarks_readed_percent_avg=Avg('bookmarks_readed_percent'),
            bookmarks_favorite_percent_avg=Avg('bookmarks_favorite_percent'),
            bookmarks_another_percent_avg=Avg('bookmarks_another_percent'),
        )
        
        rating = res.aggregate(
            rating_count_avg=Avg('rating_count'),
            rating_1_percent_avg=Avg('rating_1_percent'),
            rating_2_percent_avg=Avg('rating_2_percent'),
            rating_3_percent_avg=Avg('rating_3_percent'),
            rating_4_percent_avg=Avg('rating_4_percent'),
            rating_5_percent_avg=Avg('rating_5_percent'),
            rating_6_percent_avg=Avg('rating_6_percent'),
            rating_7_percent_avg=Avg('rating_7_percent'),
            rating_8_percent_avg=Avg('rating_8_percent'),
            rating_9_percent_avg=Avg('rating_9_percent'),
            rating_10_percent_avg=Avg('rating_10_percent'),
        )
        data = {
            'bookmarks': {key:round(value, 3) for key, value in bookmarks.items()},
            'rating': {key:round(value, 3) for key, value in rating.items()},
            'len(stats)': len(stats),
            }
        
        end = time.time()
        duration = end-start
        ic(duration)
        cls.meta_data = data

        return cls.meta_data
        
    def get_all_comments(self) -> QuerySet:
        return Comment.objects.filter(post_page__chapter_id__manga_id=self)
    
    class Meta:
        verbose_name_plural = 'Манга'
        verbose_name = 'Манга'

    def __str__(self):
        return f'{self.name}'
    
    @property
    def href(self):
        return f'https://test-front.mangalib.me/ru/manga/{self.slug}'
    
    @property 
    def chapters_href(self):
        return f'https://api.lib.social/api/manga/{self.slug}/chapters'
    
    def get_all_chapters(self):
        q:models.QuerySet[Chapter] = self.chapters.all() # type: ignore
        assert isinstance(q, models.QuerySet)
        return q
    
    def get_all_pages(self):
        return Page.objects.filter(chapter_id__manga_id=self)
    
    @property
    def chapters_count(self):
        return self.chapters.count() # type: ignore
    
    @property
    def manga_status(self):
        return str(self.status.label) # type: ignore
    
    @property
    def translate_status(self):
        return str(self.scanlate_status.label) # type: ignore
    #total_mangas = Manga.objects.filter(prior).count()
    #logging.info(f'generate_random_mangas {total_mangas=}')
    #used_indexes = set([i for i in range(1, total_mangas + 1)])
    #random_indexes = random.sample(all_mangas, 1)
     
    @staticmethod
    def generate_random_mangas(priority=0):
        logging.info(f'Запущен generate_random_mangas с приоритетом {priority}')
        all_mangas = list(Manga.objects.values_list('pk', flat=True))
        while True:
            random_mangas = random.choices(all_mangas, k=1)
            for manga_pk in random_mangas:
                all_mangas.remove(manga_pk)
                logging.info(f'{len(all_mangas)=} {manga_pk=}')
                yield Manga.objects.get(pk=manga_pk)
            if len(all_mangas) == 0:
                if priority>0:
                    return Manga.generate_random_mangas(priority=priority-1)
                else:
                    return Manga.generate_random_mangas(priority=Manga.objects.aggregate(Max('parse_priority')).get('parse_priority__max', 0))


class Stats(models.Model):
    manga = AutoOneToOneField(Manga, primary_key=True, related_name='stats', on_delete=models.CASCADE)
    bookmarks = models.JSONField(null=True, default=None)
    rating = models.JSONField(null=True, default=None)
    last_update = models.DateTimeField(auto_now=True, editable=False)
    # https://api.lib.social/api/manga/2262--oyasumi-punpun/stats?bookmarks=true&rating=true
    
class MangaUser(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    username = models.CharField(max_length=255, null=False, unique=False)
    avatar = models.JSONField(null=True, default=None)
    class Meta:
        verbose_name_plural = 'Пользователь'
        verbose_name = 'Пользователь'

    def __str__(self):
        return f'{self.username}'
    
    def comments_href_new(self, page_num:int) -> str:
        return f'https://test-front.mangalib.me/ru/user/{self.id}/comments?page={page_num}&sort_by=id&sort_type=desc'
    
    def comments_href_old(self, page_num:int) -> str:
        return f'https://test-front.mangalib.me/ru/user/{self.id}/comments?page={page_num}'
    
class Branch(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    branch_id = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(null=False)
    teams = models.ManyToManyField(Team)
    user = models.ForeignKey(MangaUser, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Ветка'
        verbose_name = 'Ветка'

    def __str__(self):
        return f'Ветка №{self.id}'
    
class Chapter(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    manga_id = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='chapters')
    teams = models.ManyToManyField(Team)
    created_at = models.DateTimeField(null=True)
    moderated = models.ForeignKey(Moderated, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=32, null=True)
    index = models.PositiveSmallIntegerField(null=False)
    item_number = models.PositiveSmallIntegerField(null=False)
    volume = models.CharField(max_length=32, null=False)
    number = models.CharField(max_length=32, null=False)
    number_secondary = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=255, null=True)
    slug = models.CharField(max_length=255, null=True)
    branches_count = models.PositiveSmallIntegerField(null=False)
    likes_count = models.PositiveIntegerField(null=True)
    
    ids = None
    class Meta:
        verbose_name_plural = 'Глава'
        verbose_name = 'Глава'

    def __str__(self):
        return f'Глава {self.id}'
    
    @classmethod
    def random(cls):
        if cls.ids is None:
            cls.ids = tuple(cls.objects.all().values_list('pk', flat=True))
        page = cls.objects.filter(id=random.choice(cls.ids)).first()
        assert page is not None
        return page
    
    @property
    def href(self):
        return f'https://test-front.mangalib.me/ru/{self.manga_id.slug_url}/read/v{self.volume}/c{self.number}'
    
    def get_all_pages(self):
        q:models.QuerySet[Page] = self.pages.all() # type: ignore
        assert isinstance(q, models.QuerySet)
        return q
    
    def is_number_number(self):
        try:
            float(self.number)
            return True
        except ValueError:
            return False
    
    @property       
    def pages_urls(self):
        return f'https://api.lib.social/api/manga/{self.manga_id.slug_url}/chapter?number={self.number}&volume={self.volume}'
    
    @property       
    async def apages_urls(self):
        return f'https://api.lib.social/api/manga/{self.manga_id.slug_url}/chapter?number={self.number}&volume={self.volume}'         
          
class Page(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True) # id
    chapter_id = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')
    image = models.CharField(max_length=255, null=True) # image
    slug = models.PositiveSmallIntegerField(null=False) # slug
    external = models.PositiveSmallIntegerField(null=False) # external
    chunks = models.PositiveSmallIntegerField(null=False) # chunks
    ratio = models.FloatField(null=False, default=float(0.0))
    created_at = models.DateTimeField(null=False) # created_at
    updated_at = models.DateTimeField(null=True) # updated_at
    height = models.PositiveSmallIntegerField(null=False) # height
    width = models.PositiveSmallIntegerField(null=False) # width
    url = models.CharField(max_length=255, null=True) # url
    
    #chapter_id = models.PositiveIntegerField(null=False, unique=True) # chapter_id
    ids = None
    
    class Meta:
        verbose_name_plural = 'Страница'
        verbose_name = 'Страница'

    def __str__(self):
        return f'{self.id}'

    @classmethod
    def random(cls):
        if cls.ids is None:
            cls.ids = tuple(cls.objects.all().values_list('pk', flat=True))
        page = cls.objects.filter(id=random.choice(cls.ids)).first()
        assert page is not None
        return page
    
    def get_comments_href(self, page):
        return f'https://api.lib.social/api/comments?page={page}&post_id={self.chapter_id.id}&post_page={self.slug}&post_type=chapter&sort_by=votes_up&sort_type=desc'

    def get_old_comments_href(self, page):
        return f'https://mangalib.me/api/v2/comments?page={page}&post_id={self.chapter_id.id}&chapterPage={self.slug}&type=chapter&order=best'
        return f'https://api.lib.social/api/comments?page={page}&post_id={self.chapter_id.id}&post_page={self.slug}&post_type=chapter&sort_by=votes_up&sort_type=desc'
        # https://api.lib.social/api/comments?page=1&post_id=142477&post_type=chapter&post_page=5&sort_by=votes_up&sort_type=desc
        # https://mangalib.me/api/v2/comments?page=1&post_id=142477&type=chapter&order=best&chapterPage=5
        
    @property
    def img_href(self):
        return f'https://img33.imgslib.link{self.url}'
    
    @property
    def href(self):
        return f'{self.chapter_id.href}?p={self.slug}'
    
    @property
    @sync_to_async
    def ahref(self):
        return f'{self.chapter_id.href}?p={self.slug}'
       
       
class Emotion(models.Model):
    name = models.CharField(max_length=12, primary_key=True, unique=True)
    
    class Meta:
        verbose_name_plural = 'Эмоция'
        verbose_name = 'Эмоция'
        
    def __str__(self) -> str:
        return f'Эмоция {self.name}'
    
class CommentEmotion(models.Model):
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    power = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], unique=False)
    comment = models.OneToOneField('Comment', on_delete=models.CASCADE, related_name='comment_emotion', primary_key=True)
    
    class Meta:
        verbose_name_plural = 'Эмоция комментария'
        verbose_name = 'Эмоция комментария'
        
    def __str__(self) -> str:
        return f'{str(self.emotion)} с силой {self.power}'
     
class Comment(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, unique=True)
    root_id = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, related_name='parent_comment_foreigth_key')
    parent_comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, related_name='root_comment_foreigth_key')
    comment_level = models.PositiveSmallIntegerField(null=False)
    comment = models.TextField(null=False)
    created_at = models.DateTimeField(null=False)
    updated_at = models.DateTimeField(null=True, default=None)
    post_page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(MangaUser, on_delete=models.CASCADE, related_name='comments')
    votes_up = models.PositiveIntegerField(null=False)
    votes_down = models.PositiveIntegerField(null=False)
    relation_type = models.CharField(max_length=255)
    relation_id = models.PositiveIntegerField(null=True)
    deleted = models.PositiveSmallIntegerField(null=True, default=None)
    
    toxic = models.FloatField(null=True, default=None)

    ids = None
    
    class Meta:
        verbose_name_plural = 'Комметарий'
        verbose_name = 'Комметарий'
        
    def __str__(self):
        return f'Комментарий {str(self.user)} {self.id}'

    @classmethod
    def random(cls):
        if cls.ids is None:
            cls.ids = tuple(cls.objects.all().values_list('pk', flat=True))
        obj = cls.objects.filter(id=random.choice(cls.ids)).first()
        assert obj is not None
        return obj






















































































































