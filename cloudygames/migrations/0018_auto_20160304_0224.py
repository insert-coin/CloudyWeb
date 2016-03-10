# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0017_auto_20160304_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesession',
            name='streaming_port',
            field=models.IntegerField(),
        ),
    ]
