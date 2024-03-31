from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import MangaPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from .serializers import MangaPageSerializer, MangaPageSerializerPopulationCompressed, MangaPageSerializerToxicCompressed
 


class ListMangaPage(APIView):

    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        pages = [MangaPageSerializer(page).data for page in MangaPage.objects.all()[slice(0, 1, None)]]
        return Response(pages)
    

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