# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinical_annotations_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='focusregionannotation',
            name='ductal_carcinoma',
            field=models.BooleanField(default=False),
        ),
    ]
