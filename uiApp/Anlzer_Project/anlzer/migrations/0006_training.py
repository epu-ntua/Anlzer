# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import anlzer.models


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0005_auto_20160330_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(default=None, null=True, upload_to=anlzer.models.upload_path_handler, blank=True)),
                ('project', models.ForeignKey(to='anlzer.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
