# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0012_auto_20160224_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='users',
        ),
    ]
