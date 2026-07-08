from django import forms
from django.contrib.auth.models import User
from .models import Profile

class QuickRegistrationForm(forms.Form):
    nickname = forms.CharField(max_length=50, required=True, label="Ваш ник")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if User.objects.filter(username=nickname).exists():
            raise forms.ValidationError('Этот ник уже занят')
        return nickname

class QuickLoginForm(forms.Form):
    nickname = forms.CharField(max_length=50, label="Ваш ник")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")