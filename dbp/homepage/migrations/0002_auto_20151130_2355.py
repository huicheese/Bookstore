# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratings',
            name='feedbackid',
            field=models.ForeignKey(db_column='feedbackid', default='lololol', to='homepage.Feedbacks'),
        ),
    ]
