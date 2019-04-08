from django import forms
from django.contrib.auth import authenticate, login, logout
from painel.models import User
from django.contrib.auth.forms import UserCreationForm

from painel.models import Variavel


class LoginForm(forms.Form):
    username = forms.CharField(label='Matrícula',max_length=30)
    password = forms.CharField(label='Senha',max_length=30,widget=forms.PasswordInput)
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username):
            raise forms.ValidationError(u'Esse nome de usuário não existe')
        return username
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if authenticate(username=username,password='abc12345678abc') or authenticate(username=username,password=password):
            us=User.objects.get(username=username)
            us.set_password(password)
            us.save()
        else:
            raise forms.ValidationError(u'Senha incorreta.')
        return password
    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        return authenticate(username=username,password=password)

class VariavelForm(forms.ModelForm):
    class Meta:
        model = Variavel
        fields=['nome','valor',]
