# Generated by Django 5.0.1 on 2024-02-10 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0015_alter_manga_parse_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='likes_count',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
