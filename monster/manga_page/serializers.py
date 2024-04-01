from rest_framework import serializers
from .models import MangaPage 

 

class MangaPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MangaPage
        exclude = [
            'population_page_compressed', 
            'population_chapter_compressed', 
            'chapter_toxic_compressed',
            'comments_count',
            'page_count',
            'chapter_count',
            'page_at_chapter_avg',
            'chapter_likes_sum',
            'chapter_likes_avg',
            'comments_toxic_avg',
            'chapters_at_days_of_the_week',
            'comments_at_days_of_the_week',
            'chapters_at_24_hours',
            'comments_at_24_hours',
            ]
        
class MangaPageSerializer24(serializers.ModelSerializer):
    class Meta:
        model = MangaPage
        fields = ['chapters_at_24_hours', 'comments_at_24_hours']
        
class MangaPageSerializerDays(serializers.ModelSerializer):
    class Meta:
        model = MangaPage
        fields = ['chapters_at_days_of_the_week', 'comments_at_days_of_the_week']

class MangaPageSerializerPopulationCompressed(serializers.ModelSerializer):
    class Meta:
        model = MangaPage
        fields = ['population_page_compressed', 'population_chapter_compressed']

class MangaPageSerializerToxicCompressed(serializers.ModelSerializer):
    class Meta:
        model = MangaPage
        fields = ['chapter_toxic_compressed']
