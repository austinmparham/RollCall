# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-23 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20181023_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='face_code',
            field=models.TextField(),
        ),
    ]
