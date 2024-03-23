from rest_framework import serializers
from .models import MangaPage 



class MangaPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MangaPage
        fields = [
                'chapter_count', 
                'chapter_likes_avg', 
                'chapter_likes_sum',
                'comments_count',
                'manga',
                'page_at_chapter_avg',
                'page_count',
                ]
        fields = '__all__'