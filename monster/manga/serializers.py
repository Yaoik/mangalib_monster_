from rest_framework import serializers
from manga.models import Manga, Stats, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = ['rating', 'bookmarks']
        
        
class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = '__all__'
        
        
class PreviewMangaSerializer(serializers.ModelSerializer):
    #status = serializers.RelatedField(source='status', read_only=True)
    status = serializers.CharField(source='status.label')
    
    class Meta:
        model = Manga
        fields = ['id', 'slug', 'status', 'name', 'rus_name', 'href', 'eng_name', 'cover', 'rating', 'release_date_string']