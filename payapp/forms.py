from django import forms
from django.contrib.auth.models import User


class TransferForm(forms.Form):
    recipient_username = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    currency_choices = (
        ('EUR', 'Euro'),
        ('GBP', 'Pounds'),
        ('USD', 'Dollars'),
    )
    currency = forms.ChoiceField(choices=currency_choices, label="Select Currency")


class RequestForm(forms.Form):
    requested_username = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    currency_choices = (
        ('EUR', 'Euro'),
        ('GBP', 'Pounds'),
        ('USD', 'Dollars'),
    )
    currency = forms.ChoiceField(choices=currency_choices, label="Select Currency")
