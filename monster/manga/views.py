from django.db.models.manager import BaseManager
from django.shortcuts import render
import django_filters.rest_framework
from .serializers import MangaSerializer
from rest_framework import generics
from .models import Manga 
from rest_framework import viewsets
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from icecream import ic
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle
from .utils import q_search, q_url_to_q, comments_count, page_count, chapter_count
from .serializers import MangaSerializer, PreviewMangaSerializer, StatsSerializer
import re
from django.core.paginator import Page, Paginator
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import renderer_classes
from rest_framework.request import Request
import json
from django.utils import timezone


@api_view(['GET'])
def get_stats(request:Request) -> Response:
    return Response(Manga.make_json())

@api_view(['POST'])
def add_stats(request:Request) -> Response:
    manga_id = int(request.POST.get('manga', 0)) # type: ignore
    data_json = json.loads(request.POST.get('data', {})) # type: ignore
    serializer = StatsSerializer(data={'rating': data_json.get('rating'), 'bookmarks': data_json.get('bookmarks')})

    if serializer.is_valid(raise_exception=True):
        manga = Manga.objects.get(id=manga_id)
        if manga.stats.rating is None or manga.stats.bookmarks is None: # type: ignore
            manga.stats.rating = serializer.validated_data.get('rating') # type: ignore
            manga.stats.bookmarks = serializer.validated_data.get('bookmarks') # type: ignore
            manga.stats.save() # type: ignore
        else:
            current_time = timezone.now()
            last_update_time = manga.stats.last_update # type: ignore
            time_difference = current_time - last_update_time
            if time_difference.days > 0:
                manga.stats.rating = serializer.validated_data.get('rating') # type: ignore
                manga.stats.bookmarks = serializer.validated_data.get('bookmarks') # type: ignore
                manga.stats.save() # type: ignore
        return Response({'success': True})
    else:
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def search(request:WSGIRequest) -> Response:
    query = request.GET.get('q', False)
    page = request.GET.get('page', 1)
    ic(query)
    if query:
        query = str(query)
        
        if query.startswith(('https://mangalib.me/', 'https://test-front.mangalib.me/')):
            query = q_url_to_q(query)
        
        if len(str(query))<3:
            return Response([], status=400)
        
        manga_manager: BaseManager[Manga] = q_search(query).order_by('id')
        
        paginator = Paginator(manga_manager, 10)
        current_page: Page = paginator.page(int(page))
        
        
        res = PreviewMangaSerializer(current_page, many=True)

        return Response({'data':res.data, 'meta':{'next':current_page.has_next(), 'current': current_page.number,'previous':current_page.has_previous()}}, status=200, template_name='manga_card.html')
    
    return Response([], status=400)


@api_view(['GET'])
def manga_page_count(request:WSGIRequest, slug:str) -> Response:
    manga = Manga.objects.get(slug=slug)
    data = {}
    data['comments_count'] = comments_count(manga)
    data['page_count'] = page_count(manga)
    data['chapter_count'] = chapter_count(manga)
    return Response(data)




def manga_page(request:WSGIRequest, slug:str):
    manga = Manga.objects.get(slug=slug)
    return render(request, 'manga.html', context={'manga':manga})



