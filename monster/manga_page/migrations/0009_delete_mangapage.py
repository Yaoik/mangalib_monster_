# Generated by Django 5.0.1 on 2024-03-20 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manga_page', '0008_remove_mangapage_least_popular_chapter_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MangaPage',
        ),
    ]
