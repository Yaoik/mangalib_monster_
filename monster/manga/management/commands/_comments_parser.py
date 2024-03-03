import json
from typing import Any, Coroutine 
import cfscrape
import time
from requests import Response
import requests
import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
import random
from urllib.parse import urlencode
import concurrent.futures
from manga.models import Manga, Chapter, Page, Moderated, Team, Comment


class CommentsParser:
    def __init__(self) -> None:
        self.scraper = cfscrape.create_scraper()
        self.death_code = [404, 422]
        self.loop = asyncio.get_event_loop()
    
    async def create_loop(self):
        self.loop = asyncio.get_running_loop()
        
    def _fetch_data(self, url, headers=None):
        while True:
            try:
                response = self.scraper.get(url, timeout=10)
                if response.status_code in self.death_code:
                    logging.warning(f'{url=}\t{response.status_code=}')
                    return None
                if response.status_code == 429:
                    time_sleep = float(response.headers.get("Retry-After", random.random()+random.random()))/2
                    logging.warning(f'{url=}\t{response.status_code=}\t{time_sleep}s\t{headers is None=}')
                    time.sleep(time_sleep)
                    return self._fetch_data(url)
                if response.status_code >= 500:
                    logging.warning(f'{url=}\t{response.status_code=}\t{32}s')
                    time.sleep(32)
                    return self._fetch_data(url)
                assert response.status_code < 300 or response.status_code >= 500, f'\n{response.url}\n{response.status_code=}'
                logging.info(f'response {url} {response.status_code}')
                return response.json()
            except KeyboardInterrupt:
                raise Exception(url)
            except requests.Timeout as e:
                return self._fetch_data(url)
            except Exception as e:
                logging.error(e)
    
    async def _fetch_data_with_inputs(self, url, *args):
        return await self._fetch_data(url), args
    
    async def parse_many_pages(self, pages:list[Page]) -> dict[Page, dict]:
        data = {}
        page_num = 1
        while len(pages)>0:
            results = await self.parse_many_urls([page.get_old_comments_href(page_num) for page in pages])
            page_num+=1
            i = 0
            while len(pages)>i:
                res = results[i]
                page = pages[i]
                assert isinstance(res, dict)
                assert isinstance(page, Page)
                data.setdefault(page, {'comments':[], 'replies':[]})
                
                data[page]['comments'].extend(res.get('comments'))
                data[page]['replies'].extend(res.get('replies'))
                
                if not res.get('next_page_url'):
                    pages.remove(page)
                    results.remove(res)
                else:
                    i+=1
        return data
    
    async def parse_many_urls(self, urls:list[str]):
        await self.create_loop()
        max_workers = 128
        coroutines = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            for url in urls:
                coroutine = self.loop.run_in_executor(pool, self._fetch_data, url)
                coroutines.append(coroutine)
        results = await asyncio.gather(*coroutines)
        return results