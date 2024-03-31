from django import template
from manga.utils import get_rgb_value, comments_count, page_count, chapter_count, avg_toxic
from manga.models import Manga


register = template.Library()

@register.filter
def get_color(value):
    red, green, blue = get_rgb_value(float(value))
    return f"rgb({red}, {green}, {blue})"


@register.filter
def get_comments_count(manga:Manga):
    return comments_count(manga)

@register.filter
def get_page_count(manga:Manga):
    return page_count(manga)

@register.filter
def get_chapter_count(manga:Manga):
    return chapter_count(manga)


@register.filter
def get_avg_toxic(manga:Manga):
    return avg_toxic(manga)