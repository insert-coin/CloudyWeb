# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0014_auto_20160224_1822'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='gamesession',
            unique_together=set([('player', 'game')]),
        ),
    ]
