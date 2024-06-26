# Generated by Django 5.0.1 on 2024-03-15 16:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0037_remove_comment_manga_comme_emotion_d0a4b0_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='emotion',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='manga.commentemotion'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['emotion'], name='manga_comme_emotion_d0a4b0_idx'),
        ),
    ]
