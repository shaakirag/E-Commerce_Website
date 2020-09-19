from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Customer, Review

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = [
            'phone'
        ]

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'is_user']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control '}),
            'last_name': forms.TextInput(attrs={'class': 'form-control '}),
            'email': forms.TextInput(attrs={'class': 'form-control '}),
            'phone': forms.TextInput(attrs={'class': 'form-control '})
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': 'readonly'}),
        }

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        exclude = ['user', 'product']

        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }
