import requests
import json
import nh

def get_html(url, params=None):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        print('Error get_html')

def getbalances():
    return nh.balances()


def getprices():
    url = 'https://api2.nicehash.com/exchange/api/v2/info/prices'
    text = get_html(url)
    j = json.loads(text)

    return j

balances = getbalances()
prices = getprices()

print(balances)
print(prices)