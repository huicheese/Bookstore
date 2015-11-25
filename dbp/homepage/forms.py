from django import forms

class loginform(forms.Form):
    login = forms.CharField(label='Login ID', max_length=50)
    pw = forms.CharField(label='Password', max_length=10, widget=forms.PasswordInput)

class advsearchform(forms.Formgit ):
    author = forms.CharField(label='Author')
    publisher = forms.CharField(label='Publisher')
    title = forms.CharField(label='Title')
    subject = forms.CharField(label='Subject')