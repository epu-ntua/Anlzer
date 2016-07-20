# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 30, 12, 36, 6, 382000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
