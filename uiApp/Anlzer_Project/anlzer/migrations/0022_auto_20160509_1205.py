# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0021_auto_20160509_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(related_name='projects', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='user',
            field=models.ForeignKey(related_name='reports', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
