# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_auto_20151203_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbacks',
            name='feedback_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=models.DateTimeField(),
        ),
    ]
