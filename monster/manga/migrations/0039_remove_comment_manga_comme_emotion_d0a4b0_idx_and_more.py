# Generated by Django 5.0.1 on 2024-03-15 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0038_comment_emotion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='emotion',
        ),
    ]
