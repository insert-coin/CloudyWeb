# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0015_auto_20160224_1827'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamesession',
            old_name='player',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='playersavedata',
            old_name='player',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='gamesession',
            unique_together=set([('user', 'game')]),
        ),
    ]
