# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0014_report_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='report',
            unique_together=set([]),
        ),
    ]
