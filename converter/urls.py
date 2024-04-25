from django.urls import path, include

from converter.views import convert_currency

urlpatterns = [
    path('conversion/<str:currency1>/<str:currency2>/<amount>/', convert_currency),
]