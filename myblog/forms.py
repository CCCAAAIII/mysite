from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(label='your name',max_length=20)
