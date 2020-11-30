from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password1 = forms.CharField(max_length=20)
    password2 = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')