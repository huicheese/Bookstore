# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('isbn', models.CharField(max_length=15, serialize=False, primary_key=True, db_column='ISBN', blank=True)),
                ('title', models.CharField(max_length=50)),
                ('authors', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=50)),
                ('yearpublished', models.IntegerField(db_column='yearPublished')),
                ('stock', models.IntegerField()),
                ('price', models.TextField()),
                ('format', models.CharField(max_length=9, null=True, blank=True)),
                ('keywords', models.CharField(max_length=100, null=True, blank=True)),
                ('subject', models.CharField(max_length=100, null=True, blank=True)),
                ('picture', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Book',
                'db_table': 'books',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('fullname', models.CharField(max_length=100, db_column='fullName')),
                ('loginid', models.CharField(max_length=30, serialize=False, primary_key=True, db_column='loginID', blank=True)),
                ('pw', models.CharField(max_length=50)),
                ('majorccn', models.CharField(max_length=19, null=True, db_column='majorCCN', blank=True)),
                ('address', models.CharField(max_length=100)),
                ('phonenum', models.CharField(max_length=25, null=True, db_column='phoneNum', blank=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'db_table': 'customers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Feedbacks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('review', models.IntegerField(null=True, blank=True)),
                ('optionalcomment', models.TextField(null=True, db_column='optionalComment', blank=True)),
                ('feedback_date', models.TimeField()),
                ('isbn', models.ForeignKey(db_column='ISBN', default='978-0345803481', to='homepage.Books')),
                ('loginid', models.ForeignKey(db_column='loginID', default='mhatib', to='homepage.Customers')),
            ],
            options={
                'db_table': 'feedbacks',
                'verbose_name': 'Feedback',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qty', models.IntegerField()),
                ('isbn', models.ForeignKey(db_column='ISBN', default='978-0345803481', to='homepage.Books')),
            ],
            options={
                'db_table': 'order_items',
                'verbose_name': 'Order Item',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('oid', models.IntegerField(serialize=False, primary_key=True, blank=True)),
                ('order_date', models.DateTimeField()),
                ('order_status', models.CharField(max_length=30, null=True, blank=True)),
                ('loginid', models.ForeignKey(db_column='loginID', default='mhatib', to='homepage.Customers')),
            ],
            options={
                'verbose_name': 'Order',
                'db_table': 'orders',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(null=True, blank=True)),
                ('feedbackid', models.ForeignKey(db_column='loginID', default='lololol', to='homepage.Feedbacks')),
                ('isbn', models.ForeignKey(db_column='ISBN', default='978-0345803481', to='homepage.Books')),
                ('ratingid', models.ForeignKey(db_column='ratingID', default='mhatib', to='homepage.Customers')),
            ],
            options={
                'db_table': 'ratings',
                'verbose_name': 'Rating',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='orderitems',
            name='oid',
            field=models.ForeignKey(db_column='oid', default='1', to='homepage.Orders'),
        ),
        migrations.AlterUniqueTogether(
            name='ratings',
            unique_together=set([('isbn', 'feedbackid', 'ratingid')]),
        ),
        migrations.AlterUniqueTogether(
            name='orderitems',
            unique_together=set([('isbn', 'oid')]),
        ),
        migrations.AlterUniqueTogether(
            name='feedbacks',
            unique_together=set([('loginid', 'isbn')]),
        ),
    ]
