# Generated by Django 5.0.1 on 2024-02-03 07:29

import users.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options_remove_user_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
    ]