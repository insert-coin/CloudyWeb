# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('publisher', models.CharField(max_length=45)),
                ('max_limit', models.IntegerField()),
                ('address', models.CharField(max_length=45)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('controller', models.IntegerField()),
                ('game', models.ForeignKey(to='cloudygames.Game')),
                ('player', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerSaveData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('saved_file', models.CharField(max_length=45)),
                ('is_autosaved', models.BooleanField(default=True)),
                ('game', models.ForeignKey(to='cloudygames.Game')),
                ('player', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
