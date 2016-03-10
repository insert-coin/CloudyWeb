# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0017_auto_20160310_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='thumbnail',
        ),
        migrations.AddField(
            model_name='game',
            name='game_img',
            field=models.ImageField(default='C:\\Users\\Gaby\\Documents\\NUS\\Semester 6\\CS3284\\Project\\cloudyweb\\cloudyweb\\public\\media/game_thumbnails/default.png', upload_to='game_thumbnails'),
        ),
    ]
