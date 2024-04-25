from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm2(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    currency_choices = (
        ('EUR', 'Euro'),
        ('GBP', 'Pounds'),
        ('DOL', 'Dollars'),
    )
    currency = forms.ChoiceField(choices=currency_choices, label="Select Currency")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'currency')

    def __init__(self, *args, **kwargs):
        super(SignUpForm2, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = None
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
