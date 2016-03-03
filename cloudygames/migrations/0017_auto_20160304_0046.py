# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0016_auto_20160224_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamesession',
            name='streaming_port',
            field=models.CharField(max_length=5, default=30000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playersavedata',
            name='is_autosaved',
            field=models.BooleanField(default=False),
        ),
    ]
