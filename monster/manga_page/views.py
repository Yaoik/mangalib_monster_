from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import MangaPage
from manga.models import Manga
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from .serializers import MangaPageSerializer, MangaPageSerializerCommentsAt, MangaPageSerializerPopulationCompressed, MangaPageSerializerToxicCompressed, MangaPageSerializerDays, MangaPageSerializer24
from django.shortcuts import render, redirect
from django.urls import reverse

class ListMangaPage(APIView):

    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        pages = [MangaPageSerializer(page).data for page in MangaPage.objects.all()[slice(0, 1, None)]]
        return Response(pages)
    
    
@api_view(['GET'])
def go_to_manga(request:Request, slug_url:str):
    manga = Manga.objects.filter(slug_url=slug_url)
    if manga.exists():
        manga = manga.first()
        assert isinstance(manga, Manga)
        return redirect(f'{reverse("manga:manga", manga.slug)}')
    return 

@api_view(['GET'])
def get_comment_at(request:Request, slug:str) -> Response:
    page = MangaPage.objects.get(manga__slug=slug)
    return Response(MangaPageSerializerCommentsAt(page).data)


@api_view(['GET'])
def get_24(request:Request, slug:str) -> Response:
    page = MangaPage.objects.get(manga__slug=slug)
    return Response(MangaPageSerializer24(page).data)

@api_view(['GET'])
def get_at_days(request:Request, slug:str) -> Response:
    page = MangaPage.objects.get(manga__slug=slug)
    return Response(MangaPageSerializerDays(page).data)

@api_view(['GET'])
def get_at_days_percent(request:Request, slug:str) -> Response:
    page = MangaPage.objects.get(manga__slug=slug)
    result = {}
    
    if page.chapters_at_days_of_the_week is not None:
        chapters_at_days_of_the_week_sum = sum(page.chapters_at_days_of_the_week)
        try:
            result['chapters_at_days_of_the_week_percent'] = [round(i/chapters_at_days_of_the_week_sum*100, 3) for i in page.chapters_at_days_of_the_week] # type: ignore
        except ZeroDivisionError:
            result['chapters_at_days_of_the_week_percent'] = [0.0 for _ in range(7)]
    else:
        chapters_at_days_of_the_week_sum = 0
    if page.comments_at_days_of_the_week is not None:
        comments_at_days_of_the_week_sum = sum(page.comments_at_days_of_the_week)
        try:
            result['comments_at_days_of_the_weekk_percent'] = [round(i/comments_at_days_of_the_week_sum*100, 3) for i in page.comments_at_days_of_the_week] # type: ignore
        except ZeroDivisionError:
            result['comments_at_days_of_the_weekk_percent'] = [0.0 for _ in range(7)]
    else:
        chapters_at_days_of_the_week_sum = 0
        
    avg = MangaPage.get_at_days_of_the_week_avg()
    result['chapters_at_days_of_the_week_percent_avg'] = avg['chapters_at_days_of_the_week_avg_percent']
    result['comments_at_days_of_the_weekk_percent_avg'] = avg['comments_at_days_of_the_week_avg_percent']
    return Response(result)


@api_view(['GET'])
def get_page(request:Request, slug:str) -> Response:
    page = MangaPage.objects.get(manga__slug=slug)
    return Response(MangaPageSerializer(page).data)

@api_view(['GET'])
def get_population_compressed(request:Request, slug:str) -> Response:
    page = MangaPage.objects.get(manga__slug=slug)
    return Response(MangaPageSerializerPopulationCompressed(page).data)

@api_view(['GET'])
def get_toxic_compressed(request:Request, slug:str) -> Response:
    page = MangaPage.objects.get(manga__slug=slug)
    return Response(MangaPageSerializerToxicCompressed(page).data)

