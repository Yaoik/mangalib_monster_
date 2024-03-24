from django.db.models.manager import BaseManager
from .models import Manga
from .serializers import MangaSerializer
from icecream import ic
from django.db.models import Q
import re

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
    
    result = Manga.objects.filter(q_objects)
    
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