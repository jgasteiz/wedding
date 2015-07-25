# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('artist', models.CharField(max_length=256, blank=True)),
                ('submitted_by', models.CharField(max_length=256, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
