from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from .forms import *
# Create your views here.
class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = '/'

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    a = 1