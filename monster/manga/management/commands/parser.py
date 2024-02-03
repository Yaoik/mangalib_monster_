import asyncio
from typing import Coroutine
from pyppeteer import launch
from pyppeteer_stealth import stealth
from pyppeteer.page import Page
from pyppeteer.errors import NetworkError
import json
import re
from ..commands import _options as request_options
from django.core.management.base import BaseCommand, CommandError
import logging
import time

logging.basicConfig(level=logging.INFO, filename=f"logs\\pars_py_log_{time.time()}.log", filemode="w+", format="%(asctime)s %(levelname)s %(message)s")

_api = [
    'https://mangalib.me/api/v2/comments?type=chapter&post_id=2551247&order=best&page=1&chapterPage=26',
    'https://mangalib.me/api/v2/test',
    'https://mangalib.me/api/comments/branch?comment_id={id}',
    'https://lib.social/api/forum/discussion?category=all&subscription=0&page=1&sort=newest',
    'https://mangalib.me/user?comm_id=173519921&section=comments',
]

_url = 'https://mangalib.me/naruto?section=chapters'
URL = 'https://mangalib.me/api/v2/comments?type=chapter&post_id=86908&order=best&page=1&chapterPage=1&user_id=425502'


class Parser:
    def __init__(self) -> None:
        self.browser = None
    
    async def initialize_browser(self):
        self.browser = await launch(headless=True)

    async def close_browser(self):
        await self.browser.close()
        
    async def parse_link(self, url):
        page:Page = await self.browser.newPage()
        await stealth(page)
        try:
            await page.goto(url)
        except NetworkError as e:
            print(f'При обработке {url}\tпроизошла ошибка: {e}')
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
                print('Запрос сделан')
                task = asyncio.create_task(self.get_json_from_page(result))
                tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        print(results)

        await self.close_browser()
    
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
    

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    
    async def main(self):
        urls = [f'https://mangalib.me/api/v2/comments?type=chapter&post_id=86908&order=best&page={i+1}&chapterPage=1&user_id=425502' for i in range(3)]

        parser = Parser()
        await parser.initialize_browser()
        
        await parser.parse_links_list(urls)
    
    
    def handle(self, *args, **options):
        asyncio.get_event_loop().run_until_complete(self.main())
    
    



