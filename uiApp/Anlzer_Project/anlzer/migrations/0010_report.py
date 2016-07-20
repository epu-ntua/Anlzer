# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anlzer', '0009_auto_20160404_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=58)),
                ('pages', models.CharField(max_length=1000)),
                ('hashtags', models.CharField(max_length=1000)),
                ('slug', models.SlugField(max_length=100, null=True)),
                ('live', models.BooleanField(default=True)),
                ('live_date_range', models.IntegerField(default=None, null=True)),
                ('start_date', models.DateField(default=None, null=True)),
                ('end_date', models.DateField(default=None, null=True)),
                ('project', models.ForeignKey(related_name='reports', to='anlzer.Project')),
                ('provider', models.ManyToManyField(to='anlzer.Provider')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
