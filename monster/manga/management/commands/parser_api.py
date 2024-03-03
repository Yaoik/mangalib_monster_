import asyncio
from copy import deepcopy
import random
import aiohttp
from typing import Any, Coroutine
import json
import re
from django.core.management.base import BaseCommand, CommandError
import logging
from logging.handlers import TimedRotatingFileHandler
import time
from asgiref.sync import sync_to_async
from django.db.models import Max, QuerySet
from manga.models import Manga, Chapter, Page, Moderated, Team, Comment
from ..commands._api_manga_parser import MangaToDb, ChaptersToDb, PagesToDB, CommentToDB, OldCommentToDB
import requests
from django.utils.dateparse import parse_datetime
import string
from ..commands._comments_parser import CommentsParser


#logging.basicConfig(level=logging.DEBUG, filename=f"logs\\pars_py_log_{time.time()}.log", filemode="w+", format="%(asctime)s %(levelname)s %(message)s", encoding='UTF-8')
#
#console_handler = logging.StreamHandler()
#console_handler.setLevel(logging.INFO)
#formatter = logging.Formatter('%(message)s')
#console_handler.setFormatter(formatter)
#
#logger = logging.getLogger()
#logger.addHandler(console_handler)


# Создание объекта логгера
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Создание TimedRotatingFileHandler
handler = TimedRotatingFileHandler(filename='logs\\pars_py_log.log', when='midnight', interval=1, backupCount=10, encoding='utf-8')
handler.setLevel(logging.DEBUG)

# Создание форматтера
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(handler)

# Добавление потокового обработчика для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(console_handler)



_api = [
    'https://mangalib.me/api/v2/comments?type=chapter&post_id=2551247&order=best&page=1&chapterPage=26',
    'https://mangalib.me/api/v2/test',
    'https://mangalib.me/api/comments/branch?comment_id={id}',
    'https://lib.social/api/forum/discussion?category=all&subscription=0&page=1&sort=newest',
    'https://mangalib.me/user?comm_id=173519921&section=comments',
    'https://mangalib.me/similar/7965?type=1',
    "https://api.lib.social/api/manga/shingeki-no-kyojin?fields[]=background&fields[]=eng_name&fields[]=otherNames&fields[]=summary&fields[]=releaseDate&fields[]=type_id&fields[]=caution&fields[]=views&fields[]=close_view&fields[]=rate_avg&fields[]=rate&fields[]=genres&fields[]=tags&fields[]=teams&fields[]=authors&fields[]=publisher&fields[]=userRating&fields[]=moderated&fields[]=metadata&fields[]=metadata.count&fields[]=metadata.close_comments&fields[]=manga_status_id&fields[]=chap_count&fields[]=status_id&fields[]=artists&fields[]=format",
    'https://api.lib.social/api/manga/247--shingeki-no-kyojin/relations',
    'https://api.lib.social/api/manga/247--shingeki-no-kyojin/similar',
    'https://api.lib.social/api/manga/247--shingeki-no-kyojin/stats?bookmarks=true&rating=true',
    'https://api.lib.social/api/manga/7965--chainsaw-man/chapters',
]

class Parser:
    def __init__(self, url:str='') -> None:
        self.main_url = url
        self.clear_url = self._clean_url(self.main_url)
        self.slug = self._get_slug(self.clear_url)
        self.data_url = self._data_url(self.slug)
        self.manga_data = False
        self.death_code = [404, 422]
        self.manga_object = None
        headers = {
            'authority': 'api.lib.social',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNDU5N2YzYmViYTdiYzU1NzZjMjUxZGQwMTBkM2ExYjU1NDIxOWVhZmU5N2VkNDIxOWI1MzZkZDg1ZWRjMWY4NTU5MDIyZTJkNDc1M2YxODciLCJpYXQiOjE3MDcyMzM5MzguMjI1MzMyLCJuYmYiOjE3MDcyMzM5MzguMjI1MzMzLCJleHAiOjE3MDk3Mzk1MzguMjE5OTE1LCJzdWIiOiI0MjU1MDIiLCJzY29wZXMiOltdfQ.Q0HCTNpoX791Y-FhvQTbrjzQ634LgrUxP6pp46da4-vbAnkdPllNZrIALOwJoevG6Haj5OkBNU415ZFmvFA9RuNqFxi7EpNFU7zNcHOqEmMVShkxpbikIRJaLv3RpAtJibLQWKsMclw0mc5FohGb6xpb7tCsIFRWP8JBfPkVUZX5Q9mS2T6Aawf0vpWNuV6go9bsihbTz8A1UXxwQ6KsROavrKLpq91f48tBNjlW71hwpLPVITVJlbhSubTioODt1BIIRYHH_T2Zk3_OMiS_4wQIgWlaCSKccWZerrJ5g-XmMMWxgspfpUm8y__x62n-T3LTxl1bSTFI8UXPXg-oGHt6rHSU1-d9nSSN8AOagHYsWvVvsiRyb-YkMXs6ItKjHyHrjohpxpMBllY58sAPp0zIavNaEIC3E4_PmZ8oyLTmTK0IJK3ofvsQV0grN04qPowDcrNE_t-RpEm3qoE3Yfl3_ZFE6ZJP94ck9ZEL-eIkbq7WeVS-qZlzjrZskXOgbgNdkH3Lhk-XMgAZwFKywMNnVZ5Gos9v4FArVcOW-vSgq3tkV4Qccx-nlYYMGg_mPbF2C9QMFiwWNn6i-k3yE2MCikm-9lqZHxQ3AWadWAKEffkH0VJiNYCQSmaDai6e8sz1m-I3ZQ5zESNQgJTzaoKFTthR_-oYfxC4Qqvdyjs',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://test-front.mangalib.me',
            'referer': 'https://test-front.mangalib.me/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'site-id': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
        self.headers = headers
        #if (x:=Manga.objects.filter(slug=self.slug)).exists():
        #    self.manga_object = x.first()
        
    @staticmethod
    def _clean_url(url:str):
        pattern = r'\?.*'
        cleaned_url = re.sub(pattern, '', url)
        return cleaned_url
    
    @staticmethod
    def _get_slug(url:str):
        return url.split('/')[-1]
    
    @staticmethod
    def _data_url(slug:str):
        return f'https://api.lib.social/api/manga/{slug}?fields[]=background&fields[]=eng_name&fields[]=otherNames&fields[]=summary&fields[]=releaseDate&fields[]=type_id&fields[]=caution&fields[]=views&fields[]=close_view&fields[]=rate_avg&fields[]=rate&fields[]=genres&fields[]=tags&fields[]=teams&fields[]=authors&fields[]=publisher&fields[]=userRating&fields[]=moderated&fields[]=metadata&fields[]=metadata.count&fields[]=metadata.close_comments&fields[]=manga_status_id&fields[]=chap_count&fields[]=status_id&fields[]=artists&fields[]=format'
    
    async def _fetch_data(self, url, headers=None):
        while True:
            try:
                #headers_t = {'authorization':headers['authorization']}
                #logging.info(headers_t)
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.get(url) as response:
                        if response.status in self.death_code:
                            logger.warning(f'{url=}\t{response.status=}')
                            return None
                        if response.status == 429:
                            time_sleep = float(response.headers.get("Retry-After", random.random()+random.random()))/2
                            logging.warning(f'{url=}\t{response.status=}\t{time_sleep}s\t{headers is None=}')
                            await asyncio.sleep(time_sleep)
                            return await self._fetch_data(url)
                        if response.status >= 500:
                            logging.warning(f'{url=}\t{response.status=}\t{32}s')
                            await asyncio.sleep(32)
                            return await self._fetch_data(url)
                        assert response.status < 300 or response.status >= 500, f'\n{response.url}\n{response.status=}'
                        logging.debug(f'response {url} ok')
                        return await response.json(encoding='UTF-8')
            except aiohttp.ClientConnectorError as e:
                logging.error(e)
    
    async def _fetch_data_with_inputs(self, url, **kwargs):
        return await self._fetch_data(url), kwargs
    
    @staticmethod
    async def _async_generator(max_concurrent:int, coroutines:list[Coroutine]):
        semaphore = asyncio.Semaphore(max_concurrent)

        async def execute_with_semaphore(coroutine):
            async with semaphore:
                return await coroutine

        for coroutine in asyncio.as_completed([execute_with_semaphore(coroutine) for coroutine in coroutines]):
            yield await coroutine

    async def _fetch_manga(self):
        self.manga_data = await self._fetch_data(self.data_url)
        if self.manga_data is None:
            return None
        return self
        
    async def parse_manga(self):
        if not isinstance(self.manga_data, dict):
            await self._fetch_manga()
        assert isinstance(self.manga_data, dict)
        manga_to_db = MangaToDb(self.manga_data)
        #manga_to_db.show()
        try:
            manga, iscreate = await manga_to_db.create_model()
        except Exception as e:
            logging.error(f'{e=}\t{manga_to_db.href=}\t{e.args=}')
            raise Exception(e)
        self.manga_object: Manga | None = manga
        return manga

    async def parse_chapters(self, manga:Manga|None=None):
        if manga is not None:
            self.manga_object = manga
        if self.manga_object is None:
            self.manga_object = await self.parse_manga()
        assert self.manga_object is not None
        data = None
        chapter_parser = None
        try:
            data = await self._fetch_data(self.manga_object.chapters_href)
            if not isinstance(data, dict):
                return
            if data.get('data') == []:
                self.manga_object.parse_priority=-1
                await self.manga_object.asave()
                logger.info(f'Приоритет {str(self.manga_object)} понижен до {self.manga_object.parse_priority}')
                return
            chapter_parser = ChaptersToDb(data, self.manga_object)
            results = await chapter_parser.create_models()
            logger.info(results)
            return results
        except AssertionError as e:
            logging.critical(e)
            logging.info(f'{data=}')
            raise AssertionError(e)
        except Exception as e:
            logging.critical(e)
            if chapter_parser is not None:
                with open('C:\\Users\\Shamrock\\Desktop\\mangalib_monster обход блокировки ботов\\monster\\manga\\management\\commands\\chapter_json.json', 'w+', encoding='UTF-8') as f:
                    f.write(chapter_parser.show())
            raise Exception(e)
    
    async def parse_pages_from_chapters(self, chapters:QuerySet[Chapter]|list[Chapter]) -> dict[Chapter, list[Page]]:
        logging.debug(f'parse_pages_from_chapters start')
        if isinstance(chapters, QuerySet):
            chapters_async = await sync_to_async(list)(chapters)
        else:
            chapters_async = chapters
        logging.debug(f'{[i.id for i in chapters_async]=}')
        coroutines = []
        for chapter in chapters_async:
            assert isinstance(chapter, Chapter)
            coroutine = self._fetch_data_with_inputs(await sync_to_async(lambda: chapter.pages_urls)(), chapter=chapter)
            coroutines.append(coroutine) # тут выполняются запросы по url
        logging.debug(f'coroutines created')
        max_concurrent = 2
        tasks = []
        async for result in self._async_generator(max_concurrent, coroutines): # генератор, выдающий результаты _fetch_data 
            if not result[0] is None:
                chapter = result[1].get('chapter')
                result = result[0]
                task = asyncio.create_task(self.parse_pages_from_chapter(result, chapter)) # сюда мне нужно передавать Chapter относящийся к этому запросу
                tasks.append(task)
        results = await asyncio.gather(*tasks)
        result_dict = {}
        for result in results:
            if isinstance(result, dict):
                result_dict.update(result)
        logging.debug(f'parse_pages_from_chapters end')
        return result_dict
    
    async def parse_pages_from_chapter(self, chapter:dict[Any, Any], chapter_model:Chapter) -> dict[Chapter, list[Page]]:
        logging.debug(f'parse_pages_from_chapter start')
        assert isinstance(chapter_model, Chapter)
        logging.debug(f'parse_pages_from_chapter {chapter_model=}')
        #logging.debug(f'parse_pages_from_chapter {chapter.get("data")}')
        data: dict = chapter.get("data", {})
        data['manga_id'] = await Manga.objects.aget(pk=data.get('manga_id'))
        data['moderated'], is_create = await Moderated.objects.aget_or_create(id=data.get('moderated', {}).get('id'), defaults=data.get('moderated', {}))
        teams = []
        for team in data.get('teams', {}):
            logging.debug(f'{team=}')
            team, is_create = await Team.objects.aget_or_create(pk=team.get('id'), defaults=team)
            teams.append(team)
        del data['teams']
        data_chap = deepcopy(data)
        del data_chap['pages']
        logging.debug(f'{data_chap=}')
        chapter_model.created_at = data_chap.get('created_at', None)
        chapter_model.type = data_chap.get('type', None)
        chapter_model.slug = data_chap.get('slug', None)
        chapter_model.moderated = data_chap.get('moderated', None)
        chapter_model.likes_count = data_chap.get('likes_count', None)
        await chapter_model.teams.aset(teams)
        await chapter_model.asave()
        logging.debug(f'parse_pages_from_chapter asave')
        logging.debug(f'parse_pages_from_chapter {chapter_model=}')
        #PagesToDB(data.get('pages', []), chapter=chapter_model).show()
        pages = await PagesToDB(pages_json=data.get('pages', []), chapter=chapter_model).create_models()
        assert isinstance(pages, list)
        if len(pages)>0:
            assert isinstance(pages[0], Page)
        logging.debug(f'parse_pages_from_chapter end')
        return {chapter_model:pages}

    async def all_pages_from_all_chapters(self, chapters:QuerySet[Chapter]):
        chapters_async = await sync_to_async(list)(chapters)
        coroutines = []
        for chapter in chapters_async:
            assert isinstance(chapter, Chapter)
            coroutine = self.parse_comments_from_pages(chapter.get_all_pages())
            coroutines.append(coroutine)
        max_concurrent = 16
        tasks = []
        async for result in self._async_generator(max_concurrent, coroutines): 
            #task = asyncio.create_task() 
            #logging.info(f'{result=}')
            tasks.append(result)
        return tasks
        #results = await asyncio.gather(*tasks)
        
    async def parse_comments_from_pages(self, pages:QuerySet[Page]):
        pages_async = await sync_to_async(list)(pages)
        coroutines = []
        for page in pages_async:
            assert isinstance(page, Page)
            href = await sync_to_async(lambda: page.href)()
            logging.info(f'{href=}')
            coroutine = self.parse_comments_from_page(page, result_data={})
            coroutines.append(coroutine)
            
        max_concurrent = 2
        tasks = []
        async for result in self._async_generator(max_concurrent, coroutines): 
            pages_json, page = result[0], result[1]
            assert isinstance(pages_json, dict)
            assert isinstance(page, Page)
            pages_json = pages_json.get('data', {})
            assert isinstance(pages_json, dict)
            if pages_json.get('replies', None) is None or pages_json.get('root', None) is None:
                logging.critical(f'ERROR {pages_json=}')
                logging.critical(f'ERROR {page.href}')
                raise Exception('ASHFDIGVNBUHITW')
            task = asyncio.create_task(CommentToDB(pages_json=pages_json, page=page).create_models()) 
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        res = []
        for r in results:
            res.extend(r)
        return set(res)
        
    async def parse_comments_from_page(self, page:Page, i:int=1, *, result_data:dict):
        response = await self._fetch_data(page.get_comments_href(i), headers=random.choice([self.headers, None]))
        assert isinstance(response, dict)
        assert isinstance(result_data, dict)
        result_data_data:dict = result_data.setdefault('data', {})
        result_data_replies:list = result_data_data.setdefault('replies', [])
        result_data_root:list = result_data_data.setdefault('root', [])
        
        response_data = response.setdefault('data', {})
        response_replies = response_data.setdefault('replies', [])
        response_root = response_data.setdefault('root', [])
        
        result_data_replies.extend(response_replies)
        result_data_root.extend(response_root)
        
        if not response.get('meta', {}).get('has_next_page', False):
            return result_data, page
        else:
            return await self.parse_comments_from_page(page, i+1, result_data=result_data)

    async def parse_all_comments_from_manga(self, manga:Manga):
        logging.info(f'parse_all_comments_from_manga {manga=}')
        chapters = await self.parse_chapters(manga)
        assert chapters is not None, 'Нет глав'
        pages = await self.parse_pages_from_chapters(chapters)
        all_pages = []
        for chapter, pages in pages.items():
            for page in pages:
                assert isinstance(page, Page)
                all_pages.append(page)
        comment_parser = CommentsParser()
        comments_json = await comment_parser.parse_many_pages(all_pages)
        
        comment_db = OldCommentToDB()
        tasks = []
        for page, comments in comments_json.items():
            tasks.append(comment_db.create_models({page:comments}))
            
        result = []
        for i in await asyncio.gather(*tasks):
            result.extend(i)
        #comments_d = {}
        #for page, comments in comments_json.items():
        #    comments_d[page] = {'comments':[], 'replies':[]}
        #    for comment in comments.get('comments', []):
        #        comments_d[page]['comments'].append(comment)
        #    for replie in comments.get('replies', []):
        #        comments_d[page]['replies'].append(replie)
        #logging.info(f'{comments_json=}')
        return result


def manga_urls_generator(page:int):
    response = requests.get(
        f'https://api.lib.social/api/manga?fields[]=rate&fields[]=rate_avg&fields[]=userBookmark&site_id[]=1&page={page}',
    )
    if response.status_code<300:
        try:
            for manga in response.json().get('data'):
                assert isinstance(manga, dict)
                yield f"https://test-front.mangalib.me/ru/manga/{manga.get('slug')}"
        except Exception as error:
            logging.error(f'{error=}')
            return False

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    
    async def main(self):
        url = 'https://test-front.mangalib.me/ru/manga/7965--chainsaw-man?section=info'
        return await Parser('https://test-front.mangalib.me/ru/manga/160510--dou-ganbattemo-ecchi-ni-nacchau-osananajimi?ui=425502').parse_manga()
        #parser = Parser(url)
        #print(parser.clear_url)
        #print(parser.data_url)
        #assert await parser.parse_manga()

        #for page in range(60, 755, 1):
        #    logging.info(f'Начат парсинг {page} страницы')
        #    try:
        #        coroutines = [Parser(url)._fetch_manga() for url in manga_urls_generator(page)]
        #        coroutines = [c for c in coroutines if not c is None]
        #        max_concurrent = 1  # Здесь вы можете установить максимальное количество одновременно выполняющихся корутин
        #
        #        tasks = []
        #        async for result in Parser._async_generator(max_concurrent, coroutines):
        #            if not result is None:
        #                assert isinstance(result, Parser)
        #                task = asyncio.create_task(result.parse_manga())
        #                tasks.append(task)
        #        results = await asyncio.gather(*tasks)
        #        assert all([isinstance(r, Manga) for r in results])
        #        for r in results:
        #            logger.info(r)
        #    except Exception as e:
        #        logging.critical(e)
    
    def parse_chapters(self, manga:Manga):
        #for manga in Manga.generate_random_mangas(priority=Manga.objects.aggregate(Max('parse_priority')).get('parse_priority__max', 0)):
            
            assert isinstance(manga, Manga)
            if manga.get_all_chapters().count()>2 and False:
                logging.info(f'{manga.get_all_chapters().count()=}')
                manga.parse_priority = 0
                manga.save()
                #continue
            logging.info(f'Начат парсинг {manga.chapters_href} страницы')
            parser = Parser(manga.href)
            res = asyncio.get_event_loop().run_until_complete(parser.parse_chapters())
            assert isinstance(res, list)
            logging.info(f'{len(res)=}')

    def parse_pages(self, manga:Manga):
        chapters: QuerySet[Chapter] = manga.get_all_chapters()
        parser = Parser()
        logging.debug(f'{chapters=}')
        logging.debug(f'{len(chapters)=}')
        #for chapter in chapters:
        #    logging.info(f'{chapter.pages_urls} {chapter.id}')
        res = asyncio.get_event_loop().run_until_complete(parser.parse_pages_from_chapters(chapters))
        logging.info(f'{res=}')
    
    def parse_comments(self, chapter:Chapter):
        #commets = Comment.objects.all().delete()
        parser = Parser()
        res = asyncio.get_event_loop().run_until_complete(parser.parse_comments_from_pages(chapter.get_all_pages()))
        logging.info(res)
        logging.info(len(res))
    
    def full_manga_parse(self, manga:Manga):
        parser = Parser()
        #chapters = manga.get_all_chapters()
        logging.info(f'{manga.href=} {manga.id}')
        #time.sleep(3)
        #res = asyncio.get_event_loop().run_until_complete(parser.all_pages_from_all_chapters(chapters))
        #time.sleep(3)
        res = asyncio.get_event_loop().run_until_complete(parser.parse_all_comments_from_manga(manga))
        return res
        #logging.info(res)
        #logging.info(len(res))
    
    def handle(self, *args, **options):
        #manga = asyncio.get_event_loop().run_until_complete(self.main())
        #assert isinstance(manga, Manga)
        #manga = Manga.objects.get(slug_url='7965--chainsaw-man')
        #manga = Manga.objects.get(slug_url='160510--dou-ganbattemo-ecchi-ni-nacchau-osananajimi')
        #manga = Manga.objects.get(slug='chainsaw-man')
        #self.parse_pages(manga)
        #manga = Manga.objects.get(slug_url='7487--waltz')
        #manga = Manga.objects.get(name='This Gorilla Will Die In 1 Day')
        #logging.info(f'{manga=}')
        #logging.info(f'{manga.id=}')
        #.full_manga_parse(manga)
        #manga = Manga.objects.get(name='Oyasumi Punpun')
        #l = self.full_manga_parse(manga)
        #logging.info(f'{l=}')
        #logging.info(f'{len(l)=}')
        from django.db.models import Count, Q, F, Value, Func
        from django.db.models.functions import Concat
        #start = time.time()
        result = (
            Page.objects
              .values('ratio')
              .annotate(total_pages=Count('id'))
              #.filter(Q(total_comments=0) & Q(total_pages__gt=0))
            )
        #print(result)
        #end = time.time()
        #print(end-start)
        href = Concat(Value('https://test-front.mangalib.me/ru/'), 'slug_url')
                  #.filter(Q(release_date__gt=2000) & Q(release_date__lt=2010))
                  #.order_by('-total_comments')
        start = time.time()
        result = (
                Manga.objects
                  .values('id')
                  .annotate(total_comments=Count('chapters__pages__comments__id'), total_pages=Count('chapters__pages__id'))
                  .filter(Q(total_comments=0) & Q(total_pages__gt=0))
                )
        #print(result)   
        end = time.time()
        print(end-start)
        for i in result:
            manga = Manga.objects.get(id=i['id'])
            logger.info(f'{manga=}\t{manga.href}\t{i}')
            try:
                self.full_manga_parse(manga)
            except AssertionError as e:
                if e.args[0] == 'Нет глав':
                    continue
                else:
                    print(e, e.args)
                    raise e



