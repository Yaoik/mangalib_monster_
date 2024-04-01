from django.db import models
from icecream import IceCreamDebugger
import logging
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When, FloatField, BigIntegerField, IntegerField
from django.db.models.functions import Cast
from asgiref.sync import sync_to_async
from copy import deepcopy
from annoying.fields import AutoOneToOneField
from icecream import callOrValue, Source, NoSourceAvailableError
from manga.models import Manga, Page, Chapter, Comment, Emotion, CommentEmotion
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay
import time
from time import time as ttt
from django.db.models.functions import Trunc
from django.db.models.functions import ExtractHour


class MyIceCreamDebugger(IceCreamDebugger):
    
    def _format(self, callFrame, *args):
        prefix = callOrValue(self.prefix)

        callNode = Source.executing(callFrame).node
        if callNode is None:
            raise NoSourceAvailableError()

        context = self._formatContext(callFrame, callNode)
        if not hasattr(self, 'last_call'):
            self.last_call = ttt()
        if not args:
            time = self._formatTime()
            out = prefix + context + time + f'   {ttt()-self.last_call}' # type: ignore
            self.last_call = ttt()
        else:
            if not self.includeContext:
                context = ''
            out = self._formatArgs(
                callFrame, callNode, prefix, context, args)

        return out
    
ic = MyIceCreamDebugger()    
#self.last_call = time.time()

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
    
    chapters_at_24_hours = models.JSONField(default=None, null=True)
    comments_at_24_hours = models.JSONField(default=None, null=True)
    
    chapters_at_days_of_the_week_avg_percent = None
    comments_at_days_of_the_week_avg_percent = None
    
    days_of_the_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресение']
    
    def __str__(self) -> str:
        return f'Страница манги {str(self.manga)}'
    
    @classmethod
    def get_at_days_of_the_week_avg(cls):
        if cls.chapters_at_days_of_the_week_avg_percent is None:
            pages = MangaPage.objects.filter(Q(chapters_at_days_of_the_week__isnull=False) & Q(comments_at_days_of_the_week__isnull=False))
            
            averages = [0] * 7 

            for obj in pages:
                at_days_of_the_week = obj.chapters_at_days_of_the_week
                if at_days_of_the_week:
                    for i, value in enumerate(at_days_of_the_week):
                        averages[i] += value

            total_objects_count = len(pages)
            if total_objects_count > 0:
                averages = [x / total_objects_count for x in averages]

            cls.chapters_at_days_of_the_week_avg_percent = averages
            
        if cls.comments_at_days_of_the_week_avg_percent is None:
            pages = MangaPage.objects.filter(Q(chapters_at_days_of_the_week__isnull=False) & Q(comments_at_days_of_the_week__isnull=False))
            
            averages = [0] * 7 

            for obj in pages:
                at_days_of_the_week = obj.comments_at_days_of_the_week
                if at_days_of_the_week:
                    for i, value in enumerate(at_days_of_the_week):
                        averages[i] += value

            total_objects_count = len(pages)
            if total_objects_count > 0:
                averages = [x / total_objects_count for x in averages]

            cls.comments_at_days_of_the_week_avg_percent = averages
        
        chapters_at_days_of_the_week_avg_percent_sum = sum(cls.chapters_at_days_of_the_week_avg_percent)
        comments_at_days_of_the_week_avg_percent_sum = sum(cls.comments_at_days_of_the_week_avg_percent)
        
        return {'comments_at_days_of_the_week_avg_percent':[round(i/comments_at_days_of_the_week_avg_percent_sum*100, 3) for i in cls.comments_at_days_of_the_week_avg_percent], 'chapters_at_days_of_the_week_avg_percent':[round(i/chapters_at_days_of_the_week_avg_percent_sum*100, 3) for i in cls.chapters_at_days_of_the_week_avg_percent]}
            
    async def update_fields(self):
        ic()
        ic(await Comment.objects.filter(post_page__chapter_id__manga_id=self.manga).acount())
        ic(f'{str(self)}   start update_fields')
        start = time.time()
        #await self.__set_count()
        await self.asave()
        end = time.time()
        print(f'{str(self)}   end __set_count   {end-start:.3f}')
        start = time.time()
        #await self.__set_population()
        await self.asave()
        end = time.time()
        print(f'{str(self)}   end __set_population   {end-start:.3f}')
        start = time.time()
        #await self.__set_page_at_chapter_avg()
        await self.asave()
        end = time.time()
        print(f'{str(self)}   end __set_page_at_chapter_avg   {end-start:.3f}')
        start = time.time()
        #await self.__set_chapter_likes() 
        await self.asave()
        end = time.time()
        print(f'{str(self)}   end __set_chapter_likes   {end-start:.3f}')
        start = time.time()
        #await self.__set_toxic()
        await self.asave()
        end = time.time()
        print(f'{str(self)}   end __set_toxic   {end-start:.3f}')
        start = time.time()
        #await self.__set_comments_emotions()
        await self.asave()
        end = time.time()
        print(f'{str(self)}   end __set_comments_emotions   {end-start:.3f}')
        start = time.time()
        #await self.__set_at_days_of_the_week()
        await self.asave()
        end = time.time()
        print(f'{str(self)}   end __set_at_days_of_the_week   {end-start:.3f}')
        start = time.time()
        await self.__set_at_24_hours()
        await self.asave()
        end = time.time()
        print(f'{str(self)}   end __set_at_24_hours   {end-start:.3f}')
        ic(f'{str(self)}   end update_fields')
        ic()
    
    async def __set_at_24_hours(self):
        chapters = Chapter.objects.filter(manga_id=self.manga).filter(created_at__isnull=False)
        comments = Comment.objects.filter(post_page__chapter_id__in=chapters).filter(created_at__isnull=False)
        
        hourly_counts_chapters = chapters.annotate(hour=ExtractHour('created_at')).values('hour').annotate(count=Count('id')).order_by('hour')
        hourly_counts_comments = comments.annotate(hour=ExtractHour('created_at')).values('hour').annotate(count=Count('id')).order_by('hour')
        
        hourly_counts_chapters_list = [0] * 24
        hourly_counts_comments_list = [0] * 24

        # Заполним массив сгруппированными значениями
        async for item in hourly_counts_chapters.aiterator(): # type: ignore
            hourly_counts_chapters_list[item['hour']] = item['count'] 
            
        # Заполним массив сгруппированными значениями
        async for item in hourly_counts_comments.aiterator(): # type: ignore
            hourly_counts_comments_list[item['hour']] = item['count']  
            
        ic(hourly_counts_chapters_list)
        ic(hourly_counts_comments_list)

        self.chapters_at_24_hours = hourly_counts_chapters_list
        self.comments_at_24_hours = hourly_counts_comments_list
        
    async def __set_at_days_of_the_week(self):
        await self.__set_chapters_at_days_of_the_week()
        await self.__comments_at_days_of_the_week()
        
    async def __set_chapters_at_days_of_the_week(self):
        results = (Chapter.objects
            .filter(manga_id=self.manga)
            .filter(created_at__isnull=False)
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
            .filter(created_at__isnull=False)
            .annotate(weekday=ExtractWeekDay('created_at')) 
            .values('weekday')                          
            .annotate(count=Count('id'))                  
            .values('weekday', 'count')
            ) 
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
        comments  = Comment.objects.filter(post_page__chapter_id__in=chapters)
        res = comments.values('post_page__chapter_id').annotate(avg_toxic=Avg('toxic'))
        try:
            self.chapter_toxic_compressed = [round(i['avg_toxic'], 3) if i['avg_toxic'] is not None else 0.0 for i in (await sync_to_async(list)(res))]
        except Exception as e:
            ic(e)
            from neural_networks.management.commands.add_emotions_to_comments import CommentProcessor
            processor = await sync_to_async(CommentProcessor)()
            n = 0
            items_per_page = 1000
            ic()
            comments_chunck = comments.filter(toxic__isnull=True)[slice(n*items_per_page, n*items_per_page+items_per_page, None)]
            while await comments_chunck.acount()>0:
                ic()
                await processor.add_emotions_to_comments(comments_chunck)
                ic()
                n+=1
                comments_chunck = comments.filter(toxic__isnull=True)[slice(n*items_per_page, n*items_per_page+items_per_page, None)]
            res = comments.values('post_page__chapter_id').annotate(avg_toxic=Avg('toxic'))
            self.chapter_toxic_compressed = [round(i['avg_toxic'], 3) if i['avg_toxic'] is not None else 0.0 for i in (await sync_to_async(list)(res))]
        
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
                .values('id', 'url')
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
    