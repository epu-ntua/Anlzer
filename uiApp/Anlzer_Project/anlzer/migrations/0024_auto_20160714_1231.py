# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0023_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='product',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='service',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
