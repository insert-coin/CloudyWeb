# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0018_auto_20160304_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(upload_to='game_thumbnails', default='/game_thumbnails/default.png'),
        ),
    ]
