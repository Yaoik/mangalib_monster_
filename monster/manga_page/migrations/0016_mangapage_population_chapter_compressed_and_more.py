# Generated by Django 5.0.3 on 2024-03-31 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_page', '0015_alter_mangapage_comments_toxic_avg'),
    ]

    operations = [
        migrations.AddField(
            model_name='mangapage',
            name='population_chapter_compressed',
            field=models.JSONField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='mangapage',
            name='population_page_compressed',
            field=models.JSONField(default=None, null=True),
        ),
    ]