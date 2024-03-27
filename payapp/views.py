from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .forms import TransferForm



# Create your views here.
@login_required
def my_account(request):
    if request.user.is_authenticated():
        return render(request, 'payapp/myaccount.html', {'user': request.user})
    else:
        return HttpResponseForbidden("You are not authorized to view this page.")


@login_required
def make_transfer_view(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = TransferForm(request.POST)
            if form.is_valid():
                print("valid")
        else:
            form = TransferForm()

        return render(request, 'payapp/transfer.html', {'user': request.user, 'form': form})

@login_required
def request_view(request):
    return render(request, 'home.html')