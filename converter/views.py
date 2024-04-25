from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest

conversion_rates = {
    'EURO': {'DOL': 1.2, 'GBP': 0.9},
    'DOL': {'EURO': 0.8, 'GBP': 0.75},
    'GBP': {'EURO': 1.1, 'DOL': 1.33}
}


def convert_currency(request, currency1, currency2, amount):
    try:
        amount = float(amount)
    except ValueError:
        return HttpResponseBadRequest('Invalid amount')

    try:
        if currency1 not in conversion_rates or currency2 not in conversion_rates[currency1]:
            raise ValueError('Error')

        conversion_rate = conversion_rates[currency1][currency2]
        converted_amount = amount * conversion_rate
        print(converted_amount)

        response = {
            'from': currency1,
            'to': currency2,
            'converted_amount': converted_amount
        }
        print(response)
        return JsonResponse(response)

    except ValueError as e:
        return HttpResponseBadRequest(str(e))
