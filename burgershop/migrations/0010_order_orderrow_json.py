# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burgershop', '0009_remove_order_orderrow_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderrow_json',
            field=models.CharField(default='', max_length=400),
        ),
    ]
