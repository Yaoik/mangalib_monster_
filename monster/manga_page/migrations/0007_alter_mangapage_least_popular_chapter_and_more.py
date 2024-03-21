# Generated by Django 5.0.1 on 2024-03-20 20:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0045_alter_emotion_name'),
        ('manga_page', '0006_mangapage_least_popular_chapter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mangapage',
            name='least_popular_chapter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='least_popular_chapter', to='manga.chapter'),
        ),
        migrations.AlterField(
            model_name='mangapage',
            name='least_popular_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='least_popular_comment', to='manga.comment'),
        ),
        migrations.AlterField(
            model_name='mangapage',
            name='least_popular_page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='least_popular_page', to='manga.page'),
        ),
        migrations.AlterField(
            model_name='mangapage',
            name='most_popular_chapter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='most_popular_chapter', to='manga.chapter'),
        ),
        migrations.AlterField(
            model_name='mangapage',
            name='most_popular_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='most_popular_comment', to='manga.comment'),
        ),
        migrations.AlterField(
            model_name='mangapage',
            name='most_popular_page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='most_popular_page', to='manga.page'),
        ),
    ]