# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0013_remove_game_users'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='gameownership',
            unique_together=set([('user', 'game')]),
        ),
    ]
