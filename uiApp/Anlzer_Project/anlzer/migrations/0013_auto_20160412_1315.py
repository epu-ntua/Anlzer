# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0012_auto_20160411_1717'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='report',
            unique_together=set([('project', 'title')]),
        ),
    ]
