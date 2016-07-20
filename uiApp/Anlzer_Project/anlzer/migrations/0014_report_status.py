# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0013_auto_20160412_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='status',
            field=models.CharField(default=b'RECURRING', max_length=50, choices=[(b'RECURRING', b'Recurring'), (b'RUNNING', b'Running'), (b'COMPLETED', b'Completed')]),
        ),
    ]
