from django.urls import path, include

from converter.views import convert_currency

urlpatterns = [
    path('conversion/<str:from_currency>/<str:to_currency>/<float:amount>/', convert_currency, name='convert_currency'),
]