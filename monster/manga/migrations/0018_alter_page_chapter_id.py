# Generated by Django 5.0.1 on 2024-02-10 18:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0017_team_discord_team_vk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='chapter_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='manga.chapter'),
        ),
    ]