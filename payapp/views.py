from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
@login_required
def my_account(request, username):
    if request.user.username == username:
        # TODO add functionality for the transactions

        return render(request, 'payapp/myaccount.html', {'user': request.user, 'username': username})
    else:
        return HttpResponseForbidden("You are not authorized to view this page.")
