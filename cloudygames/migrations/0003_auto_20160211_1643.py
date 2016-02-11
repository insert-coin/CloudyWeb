# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0002_auto_20160128_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesession',
            name='controller',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='game',
            field=models.ForeignKey(blank=True, null=True, to='cloudygames.Game'),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='player',
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
