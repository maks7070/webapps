import datetime

import thriftpy2
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .rpc_client import rpc_call

from .forms import TransferForm, RequestForm
from .models import Wallet, Transaction, TransferRequest
from django.db import transaction
from django.contrib import messages
from .util import convert

'''
Main account page, from where you can naviaget to other pages 
'''


# Create your views here.
@login_required
def my_account(request):
    wallet = Wallet.objects.get(user=request.user)
    amount = "{:.2f}".format(wallet.balance)
    currency = wallet.currency
    if currency == 'DOL':
        currency = '$'
    elif currency == 'EURO':
        currency = '€'
    else:
        currency = '£'

    user = request.user

    user_wallet = Wallet.objects.get(user=user)
    last_10_transactions = Transaction.objects.filter(Q(sender=user_wallet) | Q(recipient=user_wallet)).order_by(
        '-date')[:7]

    return render(request, 'payapp/myaccount2.html',
                  {'user': request.user,
                   'amount': amount,
                   'tran_list': last_10_transactions,
                   'currency': currency,

                   })


'''
Function that is responsible for handling the transfers.

We use TransferForm to specify the name of the user we want to send the money to 
The amount that is specified is given in the sender currency and then if needed 
transformed into the recipient currency using REST API
'''


@login_required
@transaction.atomic
def make_transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['recipient_username']
            if request.user.username != username:
                amount = float(form.cleaned_data['amount'])
                sender_wallet = Wallet.objects.get(user=request.user)
                sender_currency = sender_wallet.currency

                try:
                    recipient = User.objects.get(username=username)
                    recipient_wallet = Wallet.objects.get(user=recipient)
                    recipient_wallet_currency = recipient_wallet.currency

                except (User.DoesNotExist, Wallet.DoesNotExist):
                    messages.error(request, 'Recipient or recipients wallet not found')
                    return render(request, 'payapp/transfer2.html', {
                        'user': request.user,
                        'form': form
                    })

                if sender_wallet.balance >= amount:
                    if sender_currency == recipient_wallet_currency:
                        converted_amount = amount
                    else:
                        converted_amount = convert(sender_currency,
                                                   recipient_wallet_currency,
                                                   amount)

                    if converted_amount is not None:
                        Transaction.objects.create(
                            sender=sender_wallet,
                            recipient=recipient_wallet,
                            amount=amount,

                            date=datetime.datetime.fromtimestamp(rpc_call())
                        )

                        sender_wallet.balance -= amount
                        recipient_wallet.balance += converted_amount
                        sender_wallet.save()
                        recipient_wallet.save()
                        messages.success(request, "Transfer successful")
                        return redirect('transfer')
                    else:
                        messages.error(request, 'Failed to convert currency')
                else:
                    messages.error(request, 'Insufficient balance')
            else:
                messages.error(request, 'You cannot send a transfer to yourself')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = TransferForm()

    return render(request, 'payapp/transfer2.html', {
        'user': request.user,
        'form': form
    })


'''
View to handle transaction requests, user specifies the username of the user they request the money from 
as well as the amount of money they requested in their currency
'''


@login_required
@transaction.atomic
def request_view(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['requested_username']
            if request.user.username != username:

                amount = float(form.cleaned_data['amount'])
                request_sender = request.user
                request_sender_wallet = Wallet.objects.get(user=request_sender)
                try:
                    request_recipient_user = User.objects.get(username=username)
                    request_recipient_user_wallet = Wallet.objects.get(user=request_recipient_user)
                except (User.DoesNotExist, Wallet.DoesNotExist):
                    messages.error(request, 'Recipient not found')
                    return render(request, 'payapp/request2.html', {
                        'user': request.user,
                        'form': form
                    })

                if request_recipient_user is not None:
                    TransferRequest.objects.create(
                        sender=request_sender_wallet,
                        recipient=request_recipient_user_wallet,
                        amount=amount,
                        date=datetime.datetime.fromtimestamp(rpc_call())
                    )
                    messages.success(request, 'Request sent')
                    redirect('request')
                else:
                    messages.error(request, 'User not found')
            else:
                messages.error(request, 'You can send transaction request to yourself')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = RequestForm()

    return render(request, 'payapp/request2.html', {'form': form})


'''
Here user can see their transaction history, both incoming and outgoing transfers, for an easier use pagination 
was added to make a better UI.
'''


@login_required
def transaction_history(request):
    current_user_wallet = Wallet.objects.get(user=request.user)

    transactions = Transaction.objects.filter(
        Q(sender=current_user_wallet) | Q(recipient=current_user_wallet)
    ).order_by('-date')

    paginator = Paginator(transactions, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'payapp/transaction_history2.html', {'page_obj': page_obj})


'''

Here user can see any active notifications that they may have, s
At the top there are all active notifications that need either accepting or rejecting 
below there is a number of past transaction requests 
'''


@login_required
def notifications_view(request):
    current_user_wallet = Wallet.objects.get(user=request.user)

    transaction_requests = TransferRequest.objects.filter(recipient=current_user_wallet, completed='no').order_by(
        '-date')

    past_transactions = TransferRequest.objects.filter(recipient=current_user_wallet).exclude(completed='no').order_by(
        '-date')

    return render(request, 'payapp/notifications2.html', {'page_obj': transaction_requests,
                                                          'past_transactions': past_transactions})


'''
Function to accept transaction request notification, it works after pressing accept button on the notification page
'''


@login_required
@transaction.atomic
def accept_transaction(request, transaction_id):
    if request.method == 'POST':
        transfer_request = get_object_or_404(TransferRequest, id=transaction_id)
        sender_wallet = transfer_request.sender
        recipient_wallet = transfer_request.recipient

        sender_currency = sender_wallet.currency
        recipient_currency = recipient_wallet.currency

        amount = transfer_request.amount
        if sender_currency == recipient_currency:
            converted_amount = amount
        else:
            converted_amount = convert(sender_currency, recipient_currency, amount)

        if converted_amount <= recipient_wallet.balance:
            sender_wallet.balance += amount
            recipient_wallet.balance -= converted_amount
            transfer_request.completed = 'yes'
            sender_wallet.save()
            recipient_wallet.save()
            transfer_request.save()

            Transaction.objects.create(
                sender=recipient_wallet,
                recipient=sender_wallet,
                amount=amount,
                date=datetime.datetime.fromtimestamp(rpc_call())
            )

        else:
            messages.error(request, 'Not enough money')

        return redirect('notifications')

    return redirect('notifications')


'''
Function which rejects transaction notifications 
'''
@login_required
@transaction.atomic
def reject_transaction(request, transaction_id):
    if request.method == 'POST':
        transfer_request = get_object_or_404(TransferRequest, id=transaction_id)
        transfer_request.completed = 'rejected'
        transfer_request.save()

        return redirect('notifications')
    return redirect('notifications')


@login_required
def profile_view(request):
    pass
