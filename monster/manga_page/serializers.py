from rest_framework import serializers
from .models import MangaPage 

 

class MangaPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MangaPage
        exclude = ['population_page_compressed', 'population_chapter_compressed']
        


class MangaPageSerializerCompressed(serializers.ModelSerializer):
    class Meta:
        model = MangaPage
        fields = ['population_page_compressed', 'population_chapter_compressed']