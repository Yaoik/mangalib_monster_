from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import MangaPage
from .serializers import MangaPageSerializer
from rest_framework.permissions import IsAuthenticated


class ListMangaPage(APIView):

    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        pages = [MangaPageSerializer(page).data for page in MangaPage.objects.all()[slice(0, 1, None)]]
        return Response(pages)