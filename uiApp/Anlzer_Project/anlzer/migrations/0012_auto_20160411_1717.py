# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0011_auto_20160408_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='end_date',
            field=models.DateField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='start_date',
            field=models.DateField(default=None, null=True, blank=True),
        ),
    ]
