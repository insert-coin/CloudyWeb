# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0021_auto_20160314_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='max_limit',
            field=models.IntegerField(default=4),
        ),
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
        migrations.AlterUniqueTogether(
            name='playersavedata',
            unique_together=set([('user', 'game')]),
        ),
        migrations.RemoveField(
            model_name='playersavedata',
            name='is_autosaved',
        ),
    ]
