
import requests
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def convert(from_currency, to_currency, amount):
    url = f"https://127.0.0.1:8000/api/conversion/{from_currency}/{to_currency}/{amount}/"

    response = requests.get(url, verify=False)
    print(response)


    if response.status_code == 200:
        data = response.json()
        converted_amount = data.get('converted_amount')

        return converted_amount
    else:
        return None