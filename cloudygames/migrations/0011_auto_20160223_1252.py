# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0010_auto_20160223_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userownsgame',
            name='game',
        ),
        migrations.RemoveField(
            model_name='userownsgame',
            name='user',
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='controller',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='player',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserOwnsGame',
        ),
    ]
