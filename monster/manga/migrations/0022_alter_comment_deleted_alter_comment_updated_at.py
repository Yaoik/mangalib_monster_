# Generated by Django 5.0.1 on 2024-02-27 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0021_comment_deleted_comment_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='deleted',
            field=models.PositiveSmallIntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
