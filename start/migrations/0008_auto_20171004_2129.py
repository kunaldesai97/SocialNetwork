# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-04 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0007_auto_20171004_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='email',
            field=models.EmailField(max_length=250, unique=True),
        ),
    ]