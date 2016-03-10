# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0019_game_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(default='settings.MEDIA_ROOT/game_thumbnails/default.png', upload_to='game_thumbnails'),
        ),
    ]
