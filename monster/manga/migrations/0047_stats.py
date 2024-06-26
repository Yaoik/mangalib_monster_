# Generated by Django 5.0.3 on 2024-03-24 11:39

import annoying.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0046_alter_comment_options_remove_manga_parse_priority'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('manga', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='stats', serialize=False, to='manga.manga')),
                ('bookmarks', models.JSONField()),
                ('rating', models.JSONField()),
            ],
        ),
    ]
