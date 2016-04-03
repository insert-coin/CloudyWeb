# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0022_auto_20160331_1413'),
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
        migrations.AlterUniqueTogether(
            name='playersavedata',
            unique_together=set([('user', 'game')]),
        ),
        migrations.RemoveField(
            model_name='playersavedata',
            name='is_autosaved',
        ),
    ]
