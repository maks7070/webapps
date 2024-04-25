from django import forms
from django.contrib.auth.models import User


class TransferForm(forms.Form):
    recipient_username = forms.CharField(max_length=100)
    amount = forms.FloatField()



class RequestForm(forms.Form):
    requested_username = forms.CharField(max_length=100)
    amount = forms.FloatField()
