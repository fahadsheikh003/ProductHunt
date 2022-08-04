import requests

class CurrencyConverter:
    def __init__(self):
        url = 'https://api.exchangerate.host/latest'
        response = requests.get(url)
        data = response.json()
        self.base = data['base']
        self.rates = data['rates']

    def convert(self, _from: str, _to: str, _amount: float):
        if _from not in self.rates or _to not in self.rates:
            return 0

        if _from != self.base:
            _amount = _amount/self.rates[_from]
        return round(_amount * self.rates[_to], 2)