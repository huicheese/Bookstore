# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='books',
            options={'managed': False, 'verbose_name': 'Book'},
        ),
        migrations.AlterModelOptions(
            name='customers',
            options={'managed': False, 'verbose_name': 'Customer'},
        ),
        migrations.AlterModelOptions(
            name='feedbacks',
            options={'managed': False, 'verbose_name': 'Feedback'},
        ),
        migrations.AlterModelOptions(
            name='orderitems',
            options={'managed': False, 'verbose_name': 'Order Item'},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'managed': False, 'verbose_name': 'Order'},
        ),
        migrations.AlterModelOptions(
            name='ratings',
            options={'managed': False, 'verbose_name': 'Rating'},
        ),
    ]
