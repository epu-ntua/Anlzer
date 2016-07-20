# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0018_auto_20160504_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextradata',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 5, 9, 31, 15, 662000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
