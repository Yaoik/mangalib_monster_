from django.db import models
from manga.models import Manga, Page, Chapter, Comment, Emotion, CommentEmotion
from annoying.fields import AutoOneToOneField
from icecream import ic
import logging
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When, FloatField, BigIntegerField, IntegerField
from django.db.models.functions import Cast
from asgiref.sync import sync_to_async
from copy import deepcopy

class MangaPage(models.Model):
    manga = AutoOneToOneField(Manga, primary_key=True, related_name='site_page', on_delete=models.CASCADE)
    update_at = models.DateTimeField(auto_now=True)
    
    comments_count = models.IntegerField(default=None, null=True)
    page_count = models.IntegerField(default=None, null=True)
    chapter_count = models.IntegerField(default=None, null=True)
    
    top_10_most_popular_comment = models.JSONField(default=None, null=True)
    top_10_least_popular_comment = models.JSONField(default=None, null=True)

    population_page = models.JSONField(default=None, null=True)
    population_chapter = models.JSONField(default=None, null=True)
 
    page_at_chapter_avg = models.DecimalField(default=None, null=True, max_digits=8, decimal_places=5)
    
    chapter_likes_sum = models.IntegerField(default=None, null=True)
    chapter_likes_avg = models.DecimalField(default=None, null=True, max_digits=12, decimal_places=8)
    
    #comments_toxic_count = models.IntegerField(default=None, null=True)
    comments_toxic_avg = models.DecimalField(default=None, null=True, max_digits=8, decimal_places=7)
    
    comments_emotions_data = models.JSONField(default=None, null=True)
    
    
    def __str__(self) -> str:
        return f'Страница манги {str(self.manga)}'

    async def update_fields(self):
        logging.info(f'{str(self)}   start update_fields')
        ic()
        await self.__set_count()
        ic()
        #await self.__set_population()
        ic()
        await self.__set_page_at_chapter_avg()
        ic()
        await self.__set_chapter_likes()
        ic()
        #await self.__set_comments_toxic()
        ic()
        await self.__set_comments_emotions()
        ic()
        logging.info(f'{str(self)}   end update_fields')
       
    
    async def __set_comments_emotions(self):
        
        if self.comments_count is None:
            await self.__set_comments_count()
            
        manga_comments = Comment.objects.filter(post_page__chapter_id__manga_id=self.manga)
        emotions = Emotion.objects.aiterator()
        
        result_sum = 0
        
        data_list = []
        async for emotion in emotions: # type: ignore[GeneralTypeIssues]
            comments = manga_comments.filter(comment_emotion__isnull=False).filter(comment_emotion__emotion=emotion)
            data_dict = {}
            
            data_dict['name'] = emotion.name
            data_dict['count'] = await comments.acount()
            result_sum += data_dict['count']
            data_dict['avg_power'] = (await comments.aaggregate(avg_power=Avg('comment_emotion__power'))).get('avg_power')
            
            res = comments.values('id', 'comment_emotion__power').order_by('-comment_emotion__power')
            res = (await sync_to_async(list)(res))[:10]
            data_dict['top_max'] = res
            
            data_list.append(data_dict)
        
        for i in data_list:
            i['%_amount'] = round(i['count'] / result_sum, 5)
        self.comments_emotions_data = deepcopy(data_list)
    
    
    async def __set_comments_toxic(self):
        #await self.__set_comments_toxic_count()
        await self.__set_comments_toxic_avg()
        
    async def __set_comments_toxic_count(self):
        comments_toxic_count = await Comment.objects.filter(post_page__chapter_id__manga_id=self.manga).filter(toxic__isnull=False).acount()
        self.comments_toxic_count = comments_toxic_count
    async def __set_comments_toxic_avg(self):
        average_toxic = await Comment.objects.filter(post_page__chapter_id__manga_id=self.manga).aaggregate(avg_toxic=Avg('toxic'))
        self.comments_toxic_avg = average_toxic.get('avg_toxic')
    
    
    async def __set_chapter_likes(self):
        await self.__set_chapter_likes_sum()
        await self.__set_chapter_likes_avg()
    
    async def __set_chapter_likes_sum(self):
        total_likes = await Chapter.objects.filter(manga_id=self.manga).aaggregate(sum_likes=Sum('likes_count'))
        self.chapter_likes_sum = total_likes.get('sum_likes')
    async def __set_chapter_likes_avg(self):
        average_likes = await Chapter.objects.filter(manga_id=self.manga).aaggregate(avg_likes=Avg('likes_count'))
        self.chapter_likes_avg = average_likes.get('avg_likes')
    
    
    async def __set_page_at_chapter_avg(self):
        chapters_dict = await (
                    Chapter.objects
                    .filter(manga_id=self.manga)
                    .annotate(pages_count=Count('pages'))
                    .aaggregate(avg_comments=Avg('pages_count'))
                    )
        self.page_at_chapter_avg = chapters_dict.get('avg_comments')
    
    
    async def __set_population(self):
        await self.__set_top_10_comment()
        await self.__set_population_page()
        await self.__set_population_chapter()
    
    async def __set_top_10_comment(self):
        comments = (
                    Comment.objects
                    .filter(post_page__chapter_id__manga_id=self.manga)
                    .values('id')
                    .annotate(rating=Cast(F('votes_up'), IntegerField())-Cast(F('votes_down'), IntegerField()))
                    )
        
        best_comments = (await sync_to_async(list)(comments.order_by('-rating')))[:10]
        worst_comments = (await sync_to_async(list)(comments.order_by('rating')))[:10]
        self.top_10_least_popular_comment = worst_comments
        self.top_10_most_popular_comment = best_comments
        
        
    async def __set_population_page(self):
        pages = (
                Page.objects
                .filter(chapter_id__manga_id=self.manga)
                .values('id')
                .annotate(comment_count=Count('comments'))
                .order_by('-comment_count')
                )
        self.population_page = (await sync_to_async(list)(pages))
        
    async def __set_population_chapter(self):
        chapters = (
                    Chapter.objects
                    .filter(manga_id=self.manga)
                    .values('id')
                    .filter(likes_count__isnull=False)
                    .order_by('-likes_count')
                    )
        self.population_chapter = (await sync_to_async(list)(chapters))
        
        
    async def __set_count(self):
        await self.__set_comments_count()
        await self.__set_page_count()
        await self.__set_chapter_count()
        
    async def __set_comments_count(self):
        self.comments_count = await Comment.objects.filter(post_page__chapter_id__manga_id=self.manga).acount()
    async def __set_page_count(self):
        self.page_count = await Page.objects.filter(chapter_id__manga_id=self.manga).acount()
    async def __set_chapter_count(self):
        self.chapter_count = await Chapter.objects.filter(manga_id=self.manga).acount()
    