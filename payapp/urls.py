from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', my_account, name='my_account'),
    path('transfer/', make_transfer_view, name='transfer'),
    path('request/', request_view, name='request'),
    path('history/', transaction_history, name='history'),
    path('notifications/', notifications_view, name='notifications'),
    path('profile/', profile_view, name='profile'),
    path('accept_transaction/<int:transaction_id>/', accept_transaction, name='accept_transaction'),
    path('reject_transaction/<int:transaction_id>/', reject_transaction, name='reject_transaction'),

]