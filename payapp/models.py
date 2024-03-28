from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=1000)


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="sent_transactions")
    recipient = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)


class TransferRequest(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transaction_requestor")
    recipient = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_payer')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
