from rest_framework import serializers


class CurrencySerializer(serializers.Serializer):
    currency1 = serializers.ChoiceField(choices=('EURO', 'DOL', 'GBP'))
    currency2 = serializers.ChoiceField(choices=('EURO', 'DOL', 'GBP'))
    amount = serializers.FloatField()
