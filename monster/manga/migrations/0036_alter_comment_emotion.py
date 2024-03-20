# Generated by Django 5.0.1 on 2024-03-15 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0035_alter_comment_emotion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='emotion',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='manga.commentemotion'),
        ),
    ]