# Generated by Django 3.1 on 2020-09-17 15:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20200917_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 17, 17, 5, 24, 524475)),
        ),
        migrations.AlterField(
            model_name='bid',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 17, 17, 5, 24, 524475)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 17, 17, 5, 24, 524475)),
        ),
    ]