# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 13:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('burgershop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='burgershop.Category'),
        ),
    ]
