from django import forms
from django.contrib.auth.models import User

from .models import Account, Keyword


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username']


class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ['name']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Вы указали разные пароли')
        return cd['password2']