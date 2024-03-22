from rest_framework import serializers
from .models import MangaPage 

class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MangaPage
        fields = '__all__'  # или перечислите поля, которые вы хотите включить в сериализацию