# Generated by Django 5.0 on 2024-01-01 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_user_watchlsit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='watchlsit',
            new_name='watchlist',
        ),
    ]
