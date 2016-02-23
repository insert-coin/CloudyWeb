# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cloudygames', '0008_auto_20160218_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerOwnsGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('game', models.ForeignKey(to='cloudygames.Game')),
                ('player', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='controller',
            field=models.IntegerField(),
        ),
    ]
