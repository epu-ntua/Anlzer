# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anlzer', '0016_auto_20160414_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtraData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.CharField(default=b'COMPANY', max_length=50, choices=[(b'COMPANY', b'Company'), (b'INDIVIDUAL', b'Individual')])),
                ('under_company', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.OneToOneField(related_name='extra_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
