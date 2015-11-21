
from django import forms

class NameForm(forms.Form):
    login = forms.CharField(label='Login ID', max_length=50)
    pw = forms.CharField(label='Password', max_length=10, widget=forms.PasswordInput)
