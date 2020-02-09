from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'edit__textarea',
                                                               'maxlength': '100',
                                                               'rows': '3'}))

    class Meta:
        model = Profile
        fields = ['description', 'image']
