from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def user_signup_view(request):
    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, ' Account Created Successfully!')
    else:

        form = SignupForm()

    return render(request, 'register/signup.html', {'form': form})


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

                    messages.success(request, 'Logged in successfully !!')

                    return HttpResponseRedirect(f'/account/')
        else:
            form = AuthenticationForm()

        return render(request, 'register/user_login.html', {'form': form})

    else:

        return redirect('my_account', username=request.user.get_username())


def logout_view(request):
    logout(request)

    return redirect('login')


def password_reset_view(request):
    pass
