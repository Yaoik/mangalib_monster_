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
from .utils import q_search, q_url_to_q
from .serializers import MangaSerializer, PreviewMangaSerializer
import re
from django.core.paginator import Page, Paginator




@api_view(['GET'])
def search(request:WSGIRequest) -> Response:
    query = request.GET.get('q', False)
    page = request.GET.get('page', 1)
    
    if query:
        query = str(query)
        ic(query)
        
        if query.startswith(('https://mangalib.me/', 'https://test-front.mangalib.me/')):
            query = q_url_to_q(query)
        
        if len(str(query))<3:
            return Response([], status=400)
        
        manga_manager: BaseManager[Manga] = q_search(query).order_by('id')
        
        paginator = Paginator(manga_manager, 10)
        current_page: Page = paginator.page(int(page))
        
        
        res = PreviewMangaSerializer(current_page, many=True)

        return Response({'data':res.data, 'meta':{'next':current_page.has_next(), 'current': current_page.number,'previous':current_page.has_previous()}}, status=200)
    
    return Response([], status=400)