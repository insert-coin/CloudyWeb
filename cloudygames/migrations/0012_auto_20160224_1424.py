# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cloudygames', '0011_auto_20160223_1252'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameOwnership',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('game', models.ForeignKey(to='cloudygames.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='controller',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='player',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
