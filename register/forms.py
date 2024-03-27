from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignupForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm Password (again)")
    currency_choices = (
        ('EUR', 'Euro'),
        ('GBP', 'Pounds'),
        ('USD', 'Dollars'),
    )
    currency = forms.ChoiceField(choices=currency_choices, label="Select Currency")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}