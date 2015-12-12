from django import forms
from django.core.exceptions import ValidationError

def validate_positive(value):
    if value <= 0:
        raise ValidationError('%s is not a positive number' % value)

class loginform(forms.Form):
    login = forms.CharField(label='Login ID', max_length=50)
    pw = forms.CharField(label='Password', max_length=10, widget=forms.PasswordInput)

class advsearchform(forms.Form):
    authors = forms.CharField(label='Authors', widget=forms.TextInput(attrs={'class' : 'form-horizontal'}))
    publisher = forms.CharField(label='Publisher')
    title = forms.CharField(label='Title')
    subject = forms.CharField(label='Subject')

class RegForm(forms.Form):
    fullname = forms.CharField(label='Full Name', max_length=100)
    loginid = forms.CharField(label='Login ID', max_length=30)
    pw = forms.CharField(label = 'Password', max_length=50, widget=forms.PasswordInput)
    cfmpw = forms.CharField(label = 'Re-enter Password', max_length=50, widget=forms.PasswordInput)
    majorccn = forms.CharField(label='Major Credit Card Number',max_length=16)
    address = forms.CharField(label ='Address', max_length=100)
    phonenum = forms.CharField(label='Phone Number', max_length=25)

class BookForm(forms.Form):
    qty = forms.IntegerField(label='Qty', validators=[validate_positive])

class ViewForm(forms.Form):
    CHOICES2 = (('1', '1',), ('2', '2',), ('3', '3',), ('4', '4',), ('5', '5',), ('6', '6',), ('7', '7',), ('8', '8',), ('9', '9',), ('10', '10',))
    num = forms.ChoiceField(label="View Top Feedbacks", widget=forms.Select, choices=CHOICES2)
    # comment = forms.CharField(label="Comments(Optional)", required=False)

class FeedbackForm(forms.Form):
    CHOICES = (('1', '1',), ('2', '2',), ('3', '3',), ('4', '4',), ('5', '5',), ('6', '6',), ('7', '7',), ('8', '8',), ('9', '9',), ('10', '10',))
    feedback = forms.ChoiceField(label="Feedback", widget=forms.Select, choices=CHOICES)
    comment = forms.CharField(label="Comments(Optional)", required=False)

class removeForm(forms.Form):
    remove = forms.BooleanField(required = False)

class checkoutForm(forms.Form):
    checkout = forms.BooleanField(required = False)
