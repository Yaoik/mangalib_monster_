from django import template
from manga.utils import get_rgb_value, comments_count, page_count, chapter_count, avg_toxic
from manga.models import Manga
from manga_page.models import MangaPage
from icecream import ic

register = template.Library()

@register.simple_tag
def get_stats():
    return MangaPage.get_stats()
