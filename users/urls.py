from django.urls import path
from .views import *
from django.contrib.auth import views as authView
app_name = 'users'
urlpatterns = [
    path('register', RegisterView.as_view(), name = 'register'),
    path('login', UserLoginView.as_view(), name = 'login'),
    path('logout', UserLogoutView.as_view(), name = 'logout'),
    path('password-change', authView.PasswordChangeView.as_view(), name = 'password_change'),
    path('password-change-done', authView.PasswordChangeDoneView.as_view(), name = 'password_change_done'),
    path('profile-update/<slug:slug>', UpdateProfileView.as_view(), name='update-profile')
]