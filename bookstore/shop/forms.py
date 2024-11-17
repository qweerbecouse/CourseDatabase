# shop/forms.py
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number')

    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    phone_number = forms.CharField(label='Номер телефона')
