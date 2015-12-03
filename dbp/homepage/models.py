# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Books(models.Model):
    isbn = models.CharField(db_column='ISBN', primary_key=True, max_length=15, blank=True, null=False)  # Field name made lowercase.
    title = models.CharField(max_length=50)
    authors = models.CharField(max_length=100)
    publisher = models.CharField(max_length=50)
    yearpublished = models.IntegerField(db_column='yearPublished')  # Field name made lowercase.
    stock = models.IntegerField()
    price = models.TextField()  # This field type is a guess.
    format = models.CharField(max_length=9, blank=True, null=True)
    keywords = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    picture = models.TextField(blank=True, null=True)

    class Meta:
        #verbose_name is to change the name of the model that is displayed in the admin page
        verbose_name = 'Book'
        managed = True
        db_table = 'books'

    #When the object is called in admin/../add it's title is shown
    def __unicode__(self):
        return u'%s' % (self.isbn)


class Customers(models.Model):
    fullname = models.CharField(db_column='fullName', max_length=100)  # Field name made lowercase.
    loginid = models.CharField(db_column='loginID', primary_key=True, max_length=30, blank=True, null=False)  # Field name made lowercase.
    pw = models.CharField(max_length=50)
    majorccn = models.CharField(db_column='majorCCN', max_length=19, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(max_length=100)
    phonenum = models.CharField(db_column='phoneNum', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Customer'
        managed = True
        db_table = 'customers'

    def __unicode__(self):
        return u'%s' % (self.loginid)

class Feedbacks(models.Model):
    #loginid = models.CharField(db_column='loginID', primary_key=True, max_length=30)  # Field name made lowercase.
    loginid = models.ForeignKey('Customers', db_column='loginID',default="mhatib")
    #isbn = models.CharField(db_column='ISBN', primary_key=True, max_length=15)  # Field name made lowercase.
    isbn = models.ForeignKey('Books', db_column='ISBN',default="978-0345803481")
    review = models.IntegerField(blank=True, null=True)
    optionalcomment = models.TextField(db_column='optionalComment', blank=True, null=True)  # Field name made lowercase.
    feedback_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Feedback'
        managed = True
        db_table = 'feedbacks'
        unique_together = (('loginid', 'isbn'),)

    def __unicode__(self):
        return u'%s, %s' % (self.loginid, self.isbn)


class OrderItems(models.Model):
    #oid = models.IntegerField(primary_key=True, blank=True, null=True)
    #isbn = models.CharField(db_column='ISBN', primary_key=True, max_length=15, blank=True, null=True)  # Field name made lowercase.
    isbn = models.ForeignKey('Books', db_column='ISBN',default="978-0345803481")
    oid = models.ForeignKey('Orders', db_column='oid',default="1")
    qty = models.IntegerField()

    class Meta:
        verbose_name = 'Order Item'
        managed = True
        db_table = 'order_items'
        unique_together = (('isbn', 'oid'),)

    def __unicode__(self):
        return u'%s, %s' % (self.isbn,self.oid)


class Orders(models.Model):
    oid = models.IntegerField(primary_key=True, blank=True, null=False)
    #loginid = models.CharField(db_column='loginID', max_length=30)  # Field name made lowercase.
    loginid = models.ForeignKey('Customers', db_column='loginID',default="mhatib")
    order_date = models.DateTimeField()
    order_status = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = 'Order'
        managed = True
        db_table = 'orders'

    def __unicode__(self):
        return u'%s' % (self.oid)

class Ratings(models.Model):
    #isbn = models.CharField(db_column='ISBN', primary_key=True, max_length=15, blank=True, null=False)  # Field name made lowercase.
    isbn = models.ForeignKey('Books', db_column='ISBN',default="978-0345803481")
    #feedbackid = models.CharField(db_column='feedbackID', primary_key=True, max_length=30, blank=True, null=False)  # Field name made lowercase.
    feedbackid = models.ForeignKey('Customers', db_column='feedbackID',default="lololol",related_name="idOfFeedbackRated")
    #ratingid = models.CharField(db_column='ratingID', primary_key=True, max_length=30, blank=True, null=False)  # Field name made lowercase.
    ratingid = models.ForeignKey('Customers', db_column='ratingID',default="mhatib",related_name="raterofFeedback")
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Rating'
        managed = True
        db_table = 'ratings'
        unique_together = (('isbn', 'feedbackid', 'ratingid'),)

    def __unicode__(self):
        return u'%s, %s, %s' % (self.isbn,self.feedbackid,self.ratingid)
