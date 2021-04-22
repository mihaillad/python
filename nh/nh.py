import requests
import lm
from datetime import datetime
from time import mktime
from hashlib import sha256
import uuid
import hmac
import json

def now():

    return datetime.now()


def balances():

    orgid = lm.orgid
    key = lm.key
    secret = lm.secret

    method = 'GET'
    path = '/main/api/v2/accounting/accounts2'
    query = ''

    now = datetime.now()
    now_ec_since_epoch = mktime(now.timetuple()) + now.microsecond / 1000000.0
    xtime = int(now_ec_since_epoch * 1000)

    xnonce = str(uuid.uuid4())

    message = bytearray(key, 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(str(xtime), 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(xnonce, 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(orgid, 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(method, 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(path, 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(query, 'utf-8')

    digest = hmac.new(bytearray(secret, 'utf-8'), message, sha256).hexdigest()
    xauth = key + ":" + digest

    url = 'https://api2.nicehash.com'
    url += path

    headers = {
        'X-Time': str(xtime),
        'X-Nonce': xnonce,
        'X-Organization-Id': orgid,
        'X-Auth': xauth,
        'X-Request-Id': str(uuid.uuid4()),
        'Content-Type': 'application/json',
        'X-User-Lang': 'ru'
        }

    r = requests.get(url, headers=headers)
    j = r.json()

    currencies = j['currencies']

    # print(total['totalBalance']) баланс непонятно как расчитываемый

    # balancecontrol = 0
    balances = {}
    for item in currencies:
        if item['totalBalance'] != '0':
            # print(item)
            balances.update({item['currency']: float(item['totalBalance'])})


    return balances


def listbalance(table):

    row = {'datetime': datetime.now().isoformat()}
    totalbalanceBTC = 0

    filename = 'F:/Python/nicehashmain/data_file.json'
    # Прочитаем последнюю строку. Потом возьмем из неё данные для анализа
    for line in open(filename, 'r'):

        lastrow = line

    lastrow = json.loads(lastrow)

    # Запишем новую строку
    with open(filename,'a+', encoding='utf-8') as file:

        for item in table:
            cur = {'balance': item['balance'],
                 'BTCprice': item['BTCprice'],
                 'BTCbalance': item['BTCbalance']
                 }
            row[item['cur']] = cur

            totalbalanceBTC += item['BTCbalance']

        row['totalbalanceBTC'] = totalbalanceBTC

        json.dump(row,file)
        file.write('\n')

    return lastrow,row


def sendorder(market,side,type,quantity):

    orgid = lm.orgid
    key = lm.key
    secret = lm.secret

    method = 'GET'
    path = '/exchange/api/v2/order'
    query = "market={}&side={}&type={}&quantity={}".format(market, side, type, quantity)

    now = datetime.now()
    now_ec_since_epoch = mktime(now.timetuple()) + now.microsecond / 1000000.0
    xtime = int(now_ec_since_epoch * 1000)

    xnonce = str(uuid.uuid4())

    message = bytearray(key, 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(str(xtime), 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(xnonce, 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(orgid, 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(method, 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(path, 'utf-8')
    message += bytearray('\x00', 'utf-8')
    message += bytearray(query, 'utf-8')

    digest = hmac.new(bytearray(secret, 'utf-8'), message, sha256).hexdigest()
    xauth = key + ":" + digest

    url = 'https://api2.nicehash.com'
    url += path

    headers = {
        'X-Time': str(xtime),
        'X-Nonce': xnonce,
        'X-Organization-Id': orgid,
        'X-Auth': xauth,
        'X-Request-Id': str(uuid.uuid4()),
        'Content-Type': 'application/json',
        'X-User-Lang': 'ru'
        }

    return
    r = requests.post(url, headers=headers)
    j = r.json()

    currencies = j['currencies']

    # print(total['totalBalance']) баланс непонятно как расчитываемый

    # balancecontrol = 0
    balances = {}
    for item in currencies:
        if item['totalBalance'] != '0':
            # print(item)
            balances.update({item['currency']: float(item['totalBalance'])})


    return balances
