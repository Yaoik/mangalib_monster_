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
from .utils import q_search
from .serializers import MangaSerializer, PreviewMangaSerializer
import re

@api_view(['GET'])
def search(request:WSGIRequest) -> Response:
    query = request.GET.get('q', False)

    if query:
        query = str(query)
        ic(query)
        if query.startswith(('https://mangalib.me/', 'https://test-front.mangalib.me/')):
            if query.startswith('https://mangalib.me/'):
                pattern = r"https:\/\/mangalib\.me\/(.*?)[(\/)(?)]"
                #https://mangalib.me/oyasumi-punpun?section=info&ui=425502
            else:
                pattern = r"https:\/\/test-front\.mangalib\.me\/[^\/]+\/manga\/[^\/]+--([^\/?]+)\?"
            ic(pattern)
                
            matches = re.findall(pattern, query)
            ic(matches)
            
            if len(matches)<1:
                return Response([], status=400)
            query = matches[0]
        
            ic(query)
        if len(str(query))<3:
            return Response([], status=400)
        
        res = q_search(query)
        
        res = PreviewMangaSerializer(res, many=True)

        return Response(res.data, status=200)
    
    return Response([], status=400)