# Generated by Django 3.1 on 2020-09-18 12:51

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_auto_20200918_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 18, 14, 51, 29, 903219)),
        ),
        migrations.AlterField(
            model_name='bid',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 18, 14, 51, 29, 903219)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 18, 14, 51, 29, 904217)),
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='watcher',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='watcher',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
