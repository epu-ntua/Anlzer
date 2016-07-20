# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0020_auto_20160509_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(related_name='project', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='user',
            field=models.ForeignKey(related_name='report', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
