# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_auto_20151201_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbacks',
            name='feedback_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
