# Generated by Django 5.0.1 on 2024-02-27 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0022_alter_comment_deleted_alter_comment_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='updated_at',
        ),
    ]
