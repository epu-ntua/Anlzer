# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0007_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
