from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import *

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password1 = forms.CharField(max_length=20)
    password2 = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')


class UpdateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.field_class='mt-10'
        self.helper.layout = Layout(
            Field("bio", css_class="single-input"),
            Field("image", css_class="single-input"),
            Field("birth_date", css_class="single-input"),
        )
        self.helper.add_input(Submit('submit', 'Update', css_class="btn btn-outline-success"))
    class Meta:
        model = UserProfileModel
        fields = ['birth_date', 'bio', 'image']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }