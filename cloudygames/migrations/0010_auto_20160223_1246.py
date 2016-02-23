# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0009_auto_20160223_1241'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PlayerOwnsGame',
            new_name='UserOwnsGame',
        ),
        migrations.RenameField(
            model_name='userownsgame',
            old_name='player',
            new_name='user',
        ),
    ]
