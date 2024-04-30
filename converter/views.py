from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from converter.serializers import CurrencySerializer

conversion_rates = {
    'EURO': {'DOL': 1.2, 'GBP': 0.9},
    'DOL': {'EURO': 0.8, 'GBP': 0.75},
    'GBP': {'EURO': 1.1, 'DOL': 1.33}
}

class CurrencyConverter(APIView):
    def get(self, request, currency1, currency2, amount):
        data = {'currency1': currency1, 'currency2': currency2, 'amount': amount}
        serializer = CurrencySerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        validated_data = serializer.validated_data

        if validated_data['currency1'] not in conversion_rates or \
                validated_data['currency2'] not in conversion_rates[validated_data['currency1']]:
            return Response({'error': 'Conversion rate not found for the given currencies'}, status=404)

        conversion_rate = conversion_rates[validated_data['currency1']][validated_data['currency2']]
        converted_amount = float(validated_data['amount']) * conversion_rate

        return Response({'converted_amount': converted_amount})


