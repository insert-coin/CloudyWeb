# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0004_auto_20160211_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesession',
            name='controller',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='game',
            field=models.ForeignKey(null=True, blank=True, to='cloudygames.Game'),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='player',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
