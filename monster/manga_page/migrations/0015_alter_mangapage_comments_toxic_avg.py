# Generated by Django 5.0.3 on 2024-03-21 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_page', '0014_alter_mangapage_comments_toxic_avg_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mangapage',
            name='comments_toxic_avg',
            field=models.DecimalField(decimal_places=6, default=None, max_digits=7, null=True),
        ),
    ]
