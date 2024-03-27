from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', my_account, name='my_account'),
    path('transfer/', make_transfer_view, name='transfer'),
    path('request/', request_view, name='request')
]