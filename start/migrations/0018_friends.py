# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-18 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0017_authgroup_authgrouppermissions_authpermission_authuser_authusergroups_authuseruserpermissions_django'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.IntegerField()),
                ('rejected', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'friends',
            },
        ),
    ]
