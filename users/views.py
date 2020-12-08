from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from .forms import *
from django.views.generic import UpdateView
from django.urls import reverse

# Create your views here.
class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = '/'

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    a = 1

class UpdateProfileView(UpdateView):
    model = UserProfileModel
    template_name = 'users/update-profile.html'
    form_class = UpdateProfileForm
    def get_success_url(self):
        return reverse('index')
    def form_valid(self, form):
        form.instance.user = self.get_object().user
        if form.is_valid():
            form.save()
        return redirect('/')
