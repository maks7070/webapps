from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import SignUpForm2
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from payapp.models import Wallet
from payapp.util import convert


# Create your views here.


# Function which handles user registration, with each user registered a new wallet associated to the user is created.
# The wallet holds information about balance and which currency the user has decided to use
def user_signup_view(request):

    if request.method == "POST":

        form = SignUpForm2(request.POST)

        if form.is_valid():
            user = form.save()
            currency = form.cleaned_data['currency']
            print(currency)
            balance = 1000

            # Each user gets the value of 1000 GBP into their account
            if currency == 'EUR':
                value = convert('GBP', 'EUR', balance)['converted_amount']
                Wallet.objects.create(user=user, balance=value, currency='EURO')
            elif currency == 'DOL':
                value = convert('GBP', 'USD', balance)['converted_amount']
                Wallet.objects.create(user=user, balance=value, currency='DOL')
            else:
                Wallet.objects.create(user=user, balance=balance, currency='GBP')

            messages.success(request, ' Account Created Successfully!')
            return HttpResponseRedirect(f'/login/')
    else:

        form = SignUpForm2()

    return render(request, 'register/signup.html', {'form': form})


# The user_login_view handles the user login through built in AuthenticationForm
def user_login_view(request):
    if not request.user.is_authenticated:

        if request.method == "POST":

            form = AuthenticationForm(request=request, data=request.POST)

            if form.is_valid():

                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)

                    #messages.success(request, 'Logged in successfully !!')

                    return HttpResponseRedirect(f'/account/')
        else:
            form = AuthenticationForm()

        return render(request, 'register/user_login.html', {'form': form})

    else:

        return HttpResponseRedirect(f'/account/')


# Function which handles the user logout from the page
def logout_view(request):
    logout(request)

    return redirect('login')


def password_reset_view(request):
    pass
