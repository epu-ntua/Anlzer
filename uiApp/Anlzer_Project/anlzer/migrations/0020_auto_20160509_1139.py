# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anlzer', '0019_userextradata_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(related_name='report', default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(related_name='project', default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
