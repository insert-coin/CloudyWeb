# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import imagekit.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('description', models.TextField()),
                ('publisher', models.CharField(max_length=45)),
                ('max_limit', models.IntegerField(default=4)),
                ('address', models.CharField(max_length=45)),
                ('thumbnail', imagekit.models.fields.ProcessedImageField(default='thumbnails/default.png', upload_to='thumbnails')),
            ],
        ),
        migrations.CreateModel(
            name='GameOwnership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('game', models.ForeignKey(to='cloudygames.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('controller', models.IntegerField()),
                ('streaming_port', models.IntegerField()),
                ('game', models.ForeignKey(to='cloudygames.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerSaveData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('saved_file', models.FileField(upload_to='save_data')),
                ('game', models.ForeignKey(to='cloudygames.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='playersavedata',
            unique_together=set([('user', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='gamesession',
            unique_together=set([('user', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='gameownership',
            unique_together=set([('user', 'game')]),
        ),
    ]
