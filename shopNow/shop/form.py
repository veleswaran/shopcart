from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Enter the UserName"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':"Enter the Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"Enter the password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"Enter the confirm password"}))
    class Meta:
        model =User
        fields =['username','email','password1','password2']