from django.db import models
import re

class Tag(models.Model):    
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    href = models.CharField(max_length=255, unique=True)
    
    class Meta:
        verbose_name_plural = 'Тег'
        verbose_name = 'Тег'
    
    def __str__(self) -> str:
        return f'{self.name}'

class Manga(models.Model):
    img = models.CharField(max_length=255, unique=True)
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name_plural = 'Манга'
        verbose_name = 'Манга'
    
    