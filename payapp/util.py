
import requests

def convert(from_currency, to_currency, amount):
    url = f"http://localhost:8000/api/conversion/{from_currency}/{to_currency}/{amount}/"

    response = requests.get(url)
    print(response)


    if response.status_code == 200:
        data = response.json()
        converted_amount = data.get('converted_amount')

        return converted_amount
    else:
        return None