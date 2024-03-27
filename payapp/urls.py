from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('<str:username>/', my_account, name='my_account'),
]