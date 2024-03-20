from django.db import models
from manga.models import Manga, Page, Chapter, Comment
from annoying.fields import AutoOneToOneField
from icecream import ic
import logging

class MangaPage(models.Model):
    manga = AutoOneToOneField(Manga, primary_key=True, related_name='site_page', on_delete=models.CASCADE)
    update_at = models.DateTimeField(auto_now=True)
    
    comments_count = models.IntegerField(default=None, null=True)
    page_count = models.IntegerField(default=None, null=True)
    chapter_count = models.IntegerField(default=None, null=True)
    
    most_popular_comment = models.OneToOneField(Comment, on_delete=models.SET_NULL, null=True)
    most_popular_page = models.OneToOneField(Page, on_delete=models.SET_NULL, null=True)
    most_popular_chapter = models.OneToOneField(Chapter, on_delete=models.SET_NULL, null=True)
    
    page_at_chapter_avg = models.DecimalField(default=None, null=True, max_digits=8, decimal_places=5)
    
    chapter_likes_sum = models.IntegerField(default=None, null=True)
    chapter_likes_avg = models.DecimalField(default=None, null=True, max_digits=12, decimal_places=8)
    
    comments_toxic_count = models.IntegerField(default=None, null=True)
    comments_toxic_avg = models.DecimalField(default=None, null=True, max_digits=8, decimal_places=7)
    
    comments_emotions_data = models.JSONField(default=None, null=True)
    
    
    def __str__(self) -> str:
        return f'Страница манги {str(self.manga)}'

    async def update_fields(self):
        logging.info(f'{str(self)}   start update_fields')
        ic()
        await self.__set_count()
        await self.__set_most_popular()
        await self.__set_page_at_chapter_avg()
        await self.__set_chapter_likes()
        await self.__set_comments_toxic()
        await self.__set_comments_emotions()
        ic()
        logging.info(f'{str(self)}   end update_fields')
       
    
    async def __set_comments_emotions(self):
        ...
    
    
    async def __set_comments_toxic(self):
        await self.__set_comments_toxic_count()
        await self.__set_comments_toxic_avg()
        
    async def __set_comments_toxic_count(self):
        ...
    async def __set_comments_toxic_avg(self):
        ...
    
    
    async def __set_chapter_likes(self):
        await self.__set_chapter_likes_sum()
        await self.__set_chapter_likes_avg()
    
    async def __set_chapter_likes_sum(self):
        ...
    async def __set_chapter_likes_avg(self):
        ...
    
    
    async def __set_page_at_chapter_avg(self):
        ...
    
    
    async def __set_most_popular(self):
        await self.__set_most_popular_comment()
        await self.__set_most_popular_page()
        await self.__set_most_popular_chapter()
    
    async def __set_most_popular_comment(self):
        ...
    async def __set_most_popular_page(self):
        ...
    async def __set_most_popular_chapter(self):
        ...
        
        
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
    