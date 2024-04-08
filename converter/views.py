from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def convert_currency(request, from_currency, to_currency, amount):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    # Fixed conversion rates
    conversion_rates = {'USD': 1, 'EUR': 0.85, 'GBP': 0.75}

    if from_currency in conversion_rates and to_currency in conversion_rates:
        converted_amount = amount / conversion_rates[from_currency] * conversion_rates[to_currency]
        converted_amount = round(converted_amount, 2)
        return JsonResponse({'converted_amount': converted_amount})
    else:
        return JsonResponse({'error': 'Invalid currency'})
