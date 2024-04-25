from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # register
    path('', user_signup_view, name='signup'),
    # login
    path('login/', user_login_view, name='login'),
    # password reset
    path('reset/', password_reset_view, name='reset_password'),
    # logout
    path('logout/', logout_view, name='logout')

]
