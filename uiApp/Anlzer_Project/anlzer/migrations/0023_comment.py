# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anlzer', '0022_auto_20160509_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=1000, null=True)),
                ('author', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(related_name='comments', to='anlzer.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
