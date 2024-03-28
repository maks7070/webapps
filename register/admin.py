from django.contrib import admin

from payapp.models import Wallet, Transaction, TransferRequest


# Register your models here.

class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'amount', 'date']


class TransactionRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'amount', 'date', 'completed']


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionsAdmin)
admin.site.register(TransferRequest, TransactionRequestAdmin)
