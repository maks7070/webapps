from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import TransferForm, RequestForm
from .models import Wallet, Transaction, TransferRequest
from django.db import transaction


# Create your views here.
@login_required
def my_account(request):
    wallet = Wallet.objects.get(user=request.user)
    amount = wallet.balance

    user = request.user
    # todo add for the last transcations to see incoming as well
    last_10_transactions = Transaction.objects.filter(sender=Wallet.objects.get(user=user)).order_by('date')[:10]
    last_10_transactions = last_10_transactions[::-1]
    return render(request, 'payapp/myaccount.html',
                  {'user': request.user, 'amount': amount, 'tran_list': last_10_transactions})


@login_required
@transaction.atomic
def make_transfer_view(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['recipient_username']
            amount = form.cleaned_data['amount']
            sender_wallet = Wallet.objects.get(user=request.user)

            if sender_wallet.balance >= amount:
                recepient = User.objects.get(username=username)
                recipient_wallet = Wallet.objects.get(user=recepient)
                Transaction.objects.create(sender=sender_wallet,
                                           recipient=recipient_wallet,
                                           amount=amount,
                                           date=timezone.now())
                sender_wallet.balance -= amount
                recipient_wallet.balance += amount
                sender_wallet.save()
                recipient_wallet.save()


        else:
            pass
            # TODO add else message

    else:
        form = TransferForm()

    return render(request, 'payapp/transfer.html', {'user': request.user, 'form': form})


@login_required
def transaction_history(request):
    current_user_wallet = Wallet.objects.get(user=request.user)

    # todo fix pagination
    transactions = Transaction.objects.filter(
        Q(sender=current_user_wallet) | Q(recipient=current_user_wallet)
    ).order_by('-date')

    paginator = Paginator(transactions, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'payapp/transaction_history.html', {'page_obj': page_obj})


@login_required
def request_view(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['recipient_username']
            amount = form.cleaned_data['amount']
            sender_wallet = Wallet.objects.get(user=request.user)
            rec = Wallet.objects.get(user=User.objects.get(username=username))
            TransferRequest.objects.create(sender=sender_wallet, recipient=rec, amount=amount, date=timezone.now())
            #todo add notification creation
    else:
        form = RequestForm()

    return render(request, 'payapp/request.html', {'form': form})
