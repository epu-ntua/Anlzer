# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0008_auto_20160404_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='project',
            field=models.ForeignKey(related_name='training', to='anlzer.Project'),
        ),
    ]
