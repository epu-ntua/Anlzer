# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0004_auto_20160330_1714'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('user', 'title')]),
        ),
    ]
