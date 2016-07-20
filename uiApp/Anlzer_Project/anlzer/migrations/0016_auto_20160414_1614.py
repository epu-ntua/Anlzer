# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0015_auto_20160414_1612'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='report',
            unique_together=set([('project', 'title')]),
        ),
    ]
