# Generated by Django 5.0.1 on 2024-03-15 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0041_remove_comment_manga_comme_emotion_d0a4b0_idx_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommentEmotion',
        ),
    ]
