from django.db.models.manager import BaseManager
from .models import Manga
from .serializers import MangaSerializer
from icecream import ic
from django.db.models import Q
import re
from manga_page.models import MangaPage
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When
from manga.models import Manga, Page, Chapter, Comment, Emotion, CommentEmotion

def get_rgb_value(number: float):
    t = 3
    normalized_number = max(0, min((number - t) / (10-t), 1))

    red = int((1 - normalized_number) * 255)
    green = int(normalized_number * 255)
    blue = 0  

    return red, green, blue



def q_search(query:str) -> BaseManager[Manga]:
    #query = SearchQuery("red tomato")

    keywords = [query]
    
    q_objects = Q()
    for token in keywords:
        q_objects |= Q(rus_name__icontains=token)
        q_objects |= Q(eng_name__icontains=token)
        q_objects |= Q(other_names__icontains=token)
        q_objects |= Q(slug__icontains=token)
        #q_objects |= Q(slug_url__icontains=token)
        q_objects |= Q(name__icontains=token)
    
    # chapters__pages__comments

    result: BaseManager[Manga] = Manga.objects.filter(q_objects)

    #result = result.annotate(comments_num=Count('chapters__pages__comments')).filter(comments_num__gt=0)

    
    #ic(len(result), result)
    
    return result
    
def q_url_to_q(query:str) -> str:
    if query.startswith('https://mangalib.me/'):
        pattern = r"https:\/\/mangalib\.me\/(.*?)[(\/)(?)]"
    else:
        pattern = r"https:\/\/test-front\.mangalib\.me\/[^\/]+\/manga\/[^\/]+--([^\/?]+)\?"
        
    matches = re.findall(pattern, query)
    
    if len(matches)<1:
        return ''
    query = matches[0]
    return query



def comments_count(manga:Manga):
    page:MangaPage = manga.site_page # type:ignore
    return Comment.objects.filter(post_page__chapter_id__manga_id=manga).count()

def page_count(manga:Manga):
    page:MangaPage = manga.site_page # type:ignore
    return Page.objects.filter(chapter_id__manga_id=manga).count()

def chapter_count(manga:Manga):
    page:MangaPage = manga.site_page # type:ignore
    return Chapter.objects.filter(manga_id=manga).count()

def avg_toxic(manga:Manga):
    page:MangaPage = manga.site_page # type:ignore
    return page.comments_toxic_avg