# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudygames', '0020_auto_20160310_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playersavedata',
            name='saved_file',
            field=models.FileField(upload_to='save_data/'),
        ),
        migrations.AlterUniqueTogether(
            name='playersavedata',
            unique_together=set([('user', 'game', 'is_autosaved')]),
        ),
    ]
