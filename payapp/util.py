import requests
from django.views.decorators.csrf import csrf_exempt

'''
Due to the requirements that the code has to compile locally and in the deployment I have decided to include both addresses 
this is the only reason. If I knew it was only deployment I would have added only https 


This is here so that if you run the server localy without security by pressing run on Django then it uses http
when the server is on deployment then it uses https

In AWS deployment there is only HTTPS 
'''


def convert(from_currency, to_currency, amount):
    urls = [
        f"https://127.0.0.1:8000/api/conversion/{from_currency}/{to_currency}/{amount}/",
        f"http://127.0.0.1:8000/api/conversion/{from_currency}/{to_currency}/{amount}/"
    ]

    for url in urls:
        try:
            response = requests.get(url, verify=False)

            if response.status_code == 200:
                data = response.json()
                converted_amount = data.get('converted_amount')
                return converted_amount
        except Exception as e:
            print(f"An error occurred: {e}")
