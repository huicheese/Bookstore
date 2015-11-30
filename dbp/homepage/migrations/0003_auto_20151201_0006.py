# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20151130_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratings',
            name='feedbackid',
            field=models.ForeignKey(related_name='idOfFeedbackRated', db_column='feedbackID', default='lololol', to='homepage.Customers'),
        ),
        migrations.AlterField(
            model_name='ratings',
            name='ratingid',
            field=models.ForeignKey(related_name='raterofFeedback', db_column='ratingID', default='mhatib', to='homepage.Customers'),
        ),
    ]
