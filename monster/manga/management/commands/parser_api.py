import asyncio
import aiohttp
from typing import Coroutine
import json
import re
from django.core.management.base import BaseCommand, CommandError
import logging
import time
logging.basicConfig(level=logging.INFO, filename=f"logs\\pars_py_log_{time.time()}.log", filemode="w+", format="%(asctime)s %(levelname)s %(message)s", encoding='UTF-8')

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
    def __init__(self) -> None:
        pass
    
    async def fetch_data(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    async def async_generator(self, max_concurrent:int, coroutines:list[Coroutine]):
        semaphore = asyncio.Semaphore(max_concurrent)

        async def execute_with_semaphore(coroutine):
            async with semaphore:
                return await coroutine

        for coroutine in asyncio.as_completed([execute_with_semaphore(c) for c in coroutines]):
            yield await coroutine

    async def func3(self, url_list):
        coroutines = [self.fetch_data(url) for url in url_list]
        max_concurrent = 32  # Здесь вы можете установить максимальное количество одновременно выполняющихся корутин

        tasks = []
        async for result in self.async_generator(max_concurrent, coroutines):
            if not result is None:
                task = asyncio.create_task(self.func2(result))
                tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    
    async def main(self):
        parser = Parser()

        
    def handle(self, *args, **options):
        asyncio.get_event_loop().run_until_complete(self.main())
    
    



