# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0002_auto_20160414_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='address',
            field=models.CharField(max_length=45),
        ),
    ]
