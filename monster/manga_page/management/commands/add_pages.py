from manga_page.models import MangaPage
from manga.models import Manga
from icecream import ic
from django.core.management.base import BaseCommand
import logging
import asyncio
from asgiref.sync import sync_to_async

@sync_to_async
def get_manga_page(manga:Manga) -> MangaPage:
    page = MangaPage.objects.select_related('manga').get_or_create(manga=manga)[0]
    return page

async def add_site_page_to_manga(manga:Manga) -> MangaPage:
    page: MangaPage = await get_manga_page(manga)

    await page.update_fields()
    
    return page



async def main():

    manga_queryset = await sync_to_async(Manga.objects.all)()
    async def wrapper(slicer: slice):
        res = manga_queryset[slicer]
        res = await sync_to_async(list)(res)
        return res
    
    #manga = await Manga.objects.aget(id=2262)
    #await add_site_page_to_manga(manga=manga)
    start_at = 20
    for manga in await wrapper(slice(start_at, 1000, None)):
        if manga.id < 79:
            continue
        ic(manga.id)
        await add_site_page_to_manga(manga=manga)






class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    
    def handle(self, *args, **options):
        asyncio.run(main())
        breakpoint()