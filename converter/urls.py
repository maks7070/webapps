from django.urls import path, include


from converter.views import CurrencyConverter

urlpatterns = [
    path('conversion/<str:currency1>/<str:currency2>/<amount>/', CurrencyConverter.as_view()),
]