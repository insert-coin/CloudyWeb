# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0007_auto_20160218_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='max_limit',
            field=models.IntegerField(),
        ),
    ]
