# Generated by Django 5.0.1 on 2024-03-20 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_page', '0004_alter_mangapage_chapter_likes_avg_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mangapage',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
