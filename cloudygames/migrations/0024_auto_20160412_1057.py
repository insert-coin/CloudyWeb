# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0023_auto_20160402_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='address',
            field=models.URLField(),
        ),
    ]
