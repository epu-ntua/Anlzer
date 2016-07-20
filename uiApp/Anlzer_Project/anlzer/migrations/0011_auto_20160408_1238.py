# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0010_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='live_date_range',
        ),
        migrations.AddField(
            model_name='report',
            name='live_range',
            field=models.CharField(default=None, max_length=100, null=True, choices=[(b'LAST_DAY', b'Previous Day'), (b'LAST_WEEK', b'Last 7 Days'), (b'LAST_MONTH', b'Last 30 Days'), (b'LAST_YEAR', b'Last Year')]),
        ),
    ]
