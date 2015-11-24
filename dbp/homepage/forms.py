
from django import forms

class NameForm(forms.Form):
    login = forms.CharField(label='Login ID', max_length=50)
    pw = forms.CharField(label='Password', max_length=10, widget=forms.PasswordInput)

class RegForm(forms.Form):
    fullname = forms.CharField(label='Full Name', max_length=100)
    loginid = forms.CharField(label='Login ID', max_length=30)
    pw = forms.CharField(label = 'Password', max_length=50, widget=forms.PasswordInput)
    cfmpw = forms.CharField(label = 'Re-enter Password', max_length=50, widget=forms.PasswordInput)
    majorccn = forms.CharField(label='Major Credit Card Number',max_length=16)
    address = forms.CharField(label ='Address', max_length=100)
    phonenum = forms.CharField(label='Phone Number', max_length=25)
