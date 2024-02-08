import asyncio
import random
import aiohttp
from typing import Coroutine
import json
import re
from django.core.management.base import BaseCommand, CommandError
import logging
import time

from django.db.models import Max
from manga.models import Manga
from ..commands._api_manga_parser import MangaToDb, ChaptersToDb
import requests

logging.basicConfig(level=logging.DEBUG, filename=f"logs\\pars_py_log_{time.time()}.log", filemode="w+", format="%(asctime)s %(levelname)s %(message)s", encoding='UTF-8')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Уровень вывода сообщений
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter)

logger = logging.getLogger()
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
        self.death_code = [404]
        self.manga_object = None
        
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
    
    async def _fetch_data(self, url):
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status in self.death_code:
                            logger.warning(f'{url=}\t{response.status=}')
                            return None
                        if response.status == 429:
                            logging.warning(f'{url=}\t{response.status=}')
                            await asyncio.sleep(float(response.headers.get('Retry-After', random.random()+random.random())))
                            return await self._fetch_data(url)
                        assert response.status < 300, f'\n{response.url}\n{response.status=}'
                        logging.debug(f'Запрос {url} сделан')
                        return await response.json(encoding='UTF-8')
            except aiohttp.ClientConnectorError as e:
                logging.error(e)
    
    
    @staticmethod
    async def _async_generator(max_concurrent:int, coroutines:list[Coroutine]):
        semaphore = asyncio.Semaphore(max_concurrent)

        async def execute_with_semaphore(coroutine):
            async with semaphore:
                return await coroutine

        for coroutine in asyncio.as_completed([execute_with_semaphore(coroutine) for coroutine in coroutines]):
            yield await coroutine

    async def func3(self, url_list):
        coroutines = [self._fetch_data(url) for url in url_list]
        coroutines = [c for c in coroutines if not c is None]
        max_concurrent = 32  # Здесь вы можете установить максимальное количество одновременно выполняющихся корутин

        tasks = []
        async for result in self._async_generator(max_concurrent, coroutines):
            if not result is None:
                task = asyncio.create_task(self.func2(result))
                tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

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

    async def parse_chapters(self):
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
        chapters = manga.get_all_chapters()
        for chapter in chapters:
            logging.info(f'{chapter.pages_urls=}')
    
    def handle(self, *args, **options):
        asyncio.get_event_loop().run_until_complete(self.main())
        manga = Manga.objects.get(name='Oyasumi Punpun')
        #self.parse_chapters(manga)
        self.parse_pages(manga)
    



