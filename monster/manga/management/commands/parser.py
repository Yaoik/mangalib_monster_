from pyppeteer.page import Page
from pyppeteer.browser import Browser
import asyncio
from typing import Coroutine
from pyppeteer import launch
from pyppeteer_stealth import stealth
from pyppeteer.errors import NetworkError
from ..commands._manga_parser import MangaParser
import json
import re
from ..commands import _options as request_options
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
]

_url = 'https://mangalib.me/naruto?section=chapters'
URL = 'https://mangalib.me/api/v2/comments?type=chapter&post_id=86908&order=best&page=1&chapterPage=1&user_id=425502'
URL = 'https://mangalib.me/naruto?section=info&ui=425502'


class Parser:
    def __init__(self) -> None:
        self.browser = None
        self.manga_parser = MangaParser()
    
    async def initialize_browser(self):
        self.browser = await launch(headless=True)

    async def close_browser(self):
        assert isinstance(self.browser, Browser)
        await self.browser.close()
        
    async def parse_link(self, url):
        assert isinstance(self.browser, Browser)
        start = time.time()
        page:Page = await self.browser.newPage()
        logging.info(f'Время запроса page: {time.time()-start}')
        start = time.time()
        await stealth(page)
        logging.info(f'Время stealth: {time.time()-start}')
        try:
            start = time.time()
            await page.goto(url)
            logging.info(f'Время page.goto: {time.time()-start}')
        except NetworkError as e:
            logging.warning(f'При обработке {url}\tпроизошла ошибка: {e}')
            return None
        return page
    
    async def async_generator(self, max_concurrent:int, coroutines:list[Coroutine]):
        semaphore = asyncio.Semaphore(max_concurrent)

        async def execute_with_semaphore(coroutine):
            async with semaphore:
                return await coroutine

        for coroutine in asyncio.as_completed([execute_with_semaphore(c) for c in coroutines]):
            yield await coroutine

    async def parse_links_list(self, url_list):
        coroutines = [self.parse_link(url) for url in url_list]
        max_concurrent = 32  # Здесь вы можете установить максимальное количество одновременно выполняющихся корутин

        tasks = []
        async for result in self.async_generator(max_concurrent, coroutines):
            if not result is None:
                task = asyncio.create_task(self.get_json_from_page(result))
                tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
        #await self.close_browser()
    
    @staticmethod
    def extract_text_between_braces(input_text:str):
        input_text = input_text.replace('\n', '')
        pattern = r"\{(.+)\}"
        match = re.search(pattern, input_text)
        if match:
            return json.loads('{'+match.group(1).strip()+'}')
        else:
            return None
    
    async def get_json_from_page(self, page:Page):
        content = await page.content()
        json_data = self.extract_text_between_braces(content)
        if json_data is not None:
            pass
            #print(json.dumps(json_data, indent=4, ensure_ascii=False))
        else:
            raise Exception('json_data вернулся пустым!')
        return json_data
    
    async def manga_parse(self, manga_url:str):
        start = time.time()
        page = await self.parse_link(manga_url)
        logging.info(f'Время запроса в сумме: {time.time()-start}')
        if page is None:raise Exception(f'page вернулся пустым! {manga_url=}')
        content = await page.content()
        res = self.manga_parser.manga_html_parser(content)
        return res


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    
    async def main(self):
        urls = [f'https://mangalib.me/api/v2/comments?type=chapter&post_id=86908&order=best&page={i+1}&chapterPage=1&user_id=425502' for i in range(3)]
        
        URL = 'https://mangalib.me/dice-roll?section=chapters&ui=425502'
        URL = 'https://mangalib.me/adabana?section=chapters&ui=425502'
        URL = 'https://mangalib.me/chainsaw-man?section=info&ui=425502'
        parser = Parser()
        await parser.initialize_browser()
        
        res = await parser.manga_parse(URL)
        print(res)
        
    def handle(self, *args, **options):
        asyncio.get_event_loop().run_until_complete(self.main())
    
    



