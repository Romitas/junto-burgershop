# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burgershop', '0007_remove_order_status_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderrow_json',
            field=models.CharField(default='', max_length=400),
        ),
    ]
