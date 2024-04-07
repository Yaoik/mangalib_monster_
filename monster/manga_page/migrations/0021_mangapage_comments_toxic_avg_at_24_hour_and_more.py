# Generated by Django 5.0.3 on 2024-04-04 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_page', '0020_mangapage_page_of_chapter_toxic_compressed'),
    ]

    operations = [
        migrations.AddField(
            model_name='mangapage',
            name='comments_toxic_avg_at_24_hour',
            field=models.JSONField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='mangapage',
            name='comments_toxic_avg_at_day_of_the_week',
            field=models.JSONField(default=None, null=True),
        ),
    ]