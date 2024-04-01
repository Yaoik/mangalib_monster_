from django.db import models
from icecream import ic
import logging
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When, FloatField, BigIntegerField, IntegerField
from django.db.models.functions import Cast
from asgiref.sync import sync_to_async
from copy import deepcopy
from annoying.fields import AutoOneToOneField
from manga.models import Manga, Page, Chapter, Comment, Emotion, CommentEmotion
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay

 
class MangaPage(models.Model):
    manga = AutoOneToOneField(Manga, primary_key=True, related_name='site_page', on_delete=models.CASCADE)
    update_at = models.DateTimeField(auto_now=True, editable=False)
    
    comments_count = models.IntegerField(default=None, null=True)
    page_count = models.IntegerField(default=None, null=True)
    chapter_count = models.IntegerField(default=None, null=True)
    
    top_10_most_popular_comment = models.JSONField(default=None, null=True)
    top_10_least_popular_comment = models.JSONField(default=None, null=True)

    population_page = models.JSONField(default=None, null=True)
    population_chapter = models.JSONField(default=None, null=True)
 
    population_page_compressed = models.JSONField(default=None, null=True)
    population_chapter_compressed = models.JSONField(default=None, null=True)
    
    chapter_toxic_compressed = models.JSONField(default=None, null=True)
    
    page_at_chapter_avg = models.DecimalField(default=None, null=True, max_digits=8, decimal_places=4)
    
    chapter_likes_sum = models.IntegerField(default=None, null=True)
    chapter_likes_avg = models.DecimalField(default=None, null=True, max_digits=12, decimal_places=4)
    
    #comments_toxic_count = models.IntegerField(default=None, null=True)
    comments_toxic_avg = models.DecimalField(default=None, null=True, max_digits=7, decimal_places=6)
    
    comments_emotions_data = models.JSONField(default=None, null=True)
    
    chapters_at_days_of_the_week = models.JSONField(default=None, null=True)
    comments_at_days_of_the_week = models.JSONField(default=None, null=True)
    
    days_of_the_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресение']
    
    def __str__(self) -> str:
        return f'Страница манги {str(self.manga)}'
    
    async def update_fields(self):
        ic()
        ic(f'{str(self)}   start update_fields')
        #await self.__set_count()
        #await self.asave()
        ic(f'{str(self)}   end __set_count')
        #await self.__set_population()
        #await self.asave()
        ic(f'{str(self)}   end __set_population')
        #await self.__set_page_at_chapter_avg()
        #await self.asave()
        ic(f'{str(self)}   end __set_page_at_chapter_avg')
        #await self.__set_chapter_likes()
        #await self.asave()
        ic(f'{str(self)}   end __set_chapter_likes')
        #await self.__set_toxic()
        #await self.asave()
        ic(f'{str(self)}   end __set_toxic')
        #await self.__set_comments_emotions()
        #await self.asave()
        ic(f'{str(self)}   end __set_comments_emotions')
        await self.__set_at_days_of_the_week()
        await self.asave()
        ic(f'{str(self)}   end __set_at_days_of_the_week')
        ic(f'{str(self)}   end update_fields')
        ic()
    
    async def __set_at_days_of_the_week(self):
        await self.__set_chapters_at_days_of_the_week()
        await self.__comments_at_days_of_the_week()
        
    async def __set_chapters_at_days_of_the_week(self):
        results = (Chapter.objects
            .filter(manga_id=self.manga)
            .annotate(weekday=ExtractWeekDay('created_at')) 
            .values('weekday')                          
            .annotate(count=Count('id'))                  
            .values('weekday', 'count')) 
        res = {i:0 for i in range(7)}
        for result in await sync_to_async(list)(results):
            if result['weekday'] == 1:
                res[6] = result['count']
            else:
                res[result['weekday']-2] = result['count']
        self.chapters_at_days_of_the_week = [value for key, value in res.items()]
         
    async def __comments_at_days_of_the_week(self):
        results = (Comment.objects
            .filter(post_page__chapter_id__manga_id=self.manga)
            .annotate(weekday=ExtractWeekDay('created_at')) 
            .values('weekday')                          
            .annotate(count=Count('id'))                  
            .values('weekday', 'count')) 
        
        res = {i:0 for i in range(7)}
        for result in await sync_to_async(list)(results):
            if result['weekday'] == 1:
                res[6] = result['count']
            else:
                res[result['weekday']-2] = result['count']
        self.comments_at_days_of_the_week = [value for key, value in res.items()]
    
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
            try:
                i['%_amount'] = round(i['count'] / result_sum, 5)
            except ZeroDivisionError:
                i['%_amount'] = 0.0
        self.comments_emotions_data = deepcopy(data_list)
    
    
    async def __set_toxic(self):
        #await self.__set_comments_toxic_count()
        await self.__set_chapter_toxic()
        await self.__set_comments_toxic_avg()
        
    async def __set_chapter_toxic(self):
        chapters = Chapter.objects.filter(manga_id=self.manga)
        comments = Comment.objects.filter(post_page__chapter_id__in=chapters)
        res = comments.values('post_page__chapter_id').annotate(avg_toxic=Avg('toxic'))
        try:
            self.chapter_toxic_compressed = [round(i['avg_toxic'], 3) for i in (await sync_to_async(list)(res))]
        except Exception as e:
            ic(e)
            from neural_networks.management.commands.add_emotions_to_comments import CommentProcessor
            processor = await sync_to_async(CommentProcessor)()
            comments = Comment.objects.filter(post_page__chapter_id__manga_id=self.manga)
            await processor.add_emotions_to_comments(comments)
            self.chapter_toxic_compressed = [round(i['avg_toxic'], 3) for i in (await sync_to_async(list)(res))]
        
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
                )

        self.population_page_compressed = [page['comment_count'] for page in await sync_to_async(list)(pages)]

        pages = (await sync_to_async(list)(pages.order_by('-comment_count')))
        self.population_page = {'most':pages[:25], 'least':pages[-25:]}
        
    async def __set_population_chapter(self):
        chapters = (
                    Chapter.objects
                    .filter(manga_id=self.manga)
                    .values('id', 'likes_count')
                    )
        chapters = (await sync_to_async(list)(chapters.order_by('-likes_count')))

        res = []
        for chapter in chapters:
            res.append((chapter['likes_count'], chapter['id']))
            
        self.population_chapter_compressed = [item[0] for item in sorted(res, key=lambda x: x[1])]
        self.population_chapter = {'most': chapters[:25], 'least':chapters[-25:]}
        
        
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
    