from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=1000)
    currency = models.CharField(max_length=5, default='GBP')


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="sent_transactions")
    recipient = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class TransferRequest(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transaction_requestor")
    recipient = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_payer')
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)



# todo add handling for notifications