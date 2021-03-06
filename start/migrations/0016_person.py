# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-17 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0015_auto_20171017_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('username', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=20, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'MALE'), ('F', 'FEMALE')], max_length=1, null=True)),
                ('emailid', models.CharField(blank=True, max_length=20, null=True, unique=True)),
            ],
            options={
                'db_table': 'person',
                'managed': False,
            },
        ),
    ]
