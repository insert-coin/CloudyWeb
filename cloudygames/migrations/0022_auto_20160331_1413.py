# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0021_auto_20160314_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(upload_to='thumbnails', default='thumbnails/default.png'),
        ),
        migrations.AlterField(
            model_name='playersavedata',
            name='saved_file',
            field=models.FileField(upload_to='save_data'),
        ),
    ]
