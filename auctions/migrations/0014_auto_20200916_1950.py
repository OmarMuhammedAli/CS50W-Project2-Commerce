# Generated by Django 3.1 on 2020-09-16 17:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20200916_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 16, 19, 50, 34, 239705)),
        ),
        migrations.AlterField(
            model_name='bid',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 16, 19, 50, 34, 240771)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 16, 19, 50, 34, 240771)),
        ),
    ]