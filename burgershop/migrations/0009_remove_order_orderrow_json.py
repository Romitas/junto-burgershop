# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 19:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('burgershop', '0008_order_orderrow_json'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='orderrow_json',
        ),
    ]
