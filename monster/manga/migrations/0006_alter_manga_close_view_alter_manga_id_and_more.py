# Generated by Django 5.0.1 on 2024-02-06 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0005_alter_manga_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='close_view',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='manga',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='manga',
            name='release_date',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='manga',
            name='site',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='people',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='user_id',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
