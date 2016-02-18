# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0003_auto_20160211_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesession',
            name='controller',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='game',
            field=models.ForeignKey(to='cloudygames.Game'),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='player',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
