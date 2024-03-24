from rest_framework import serializers
from .models import Manga 



class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = '__all__'
        
        
class PreviewMangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = ['id', 'name', 'rus_name', 'href', 'eng_name', 'cover', 'rating', 'model']