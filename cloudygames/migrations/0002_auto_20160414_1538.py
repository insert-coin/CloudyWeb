# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='address',
            field=models.URLField(),
        ),
    ]
