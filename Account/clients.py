"""
Mr.Kataei 8/4/2021
use for telegram bot to register
and exchanges account implement here
"""
import hashlib
import hmac
import json
import time
import requests

from Inc import functions


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.username = None
        self.user_setting = None
        self.strategy = None
        self.account = None

    def update_user_plan_limit(self):
        if self.username is not None:
            plan_id = functions.get_user_plan(username=self.username)
            plan = functions.record_dictionary(record=functions.get_plans(plan_id=plan_id)[0], table='plans')
            self.strategy = plan['strategy_number']
            self.account = plan['account_number']


class BitfinexClient:
    BASE_URL = "https://api.bitfinex.com/"

    def __init__(self, public: str, secret: str):
        self.__KEY = public
        self.__SECRET = secret

    def _nonce(self):
        # Returns a nonce
        # Used in authentication
        return str(int(round(time.time() * 10000)))

    def _headers(self, path, nonce, body):
        secbytes = self.__SECRET.encode(encoding='UTF-8')
        signature = "/api/" + path + nonce + body
        sigbytes = signature.encode(encoding='UTF-8')
        h = hmac.new(secbytes, sigbytes, hashlib.sha384)
        hexstring = h.hexdigest()
        return {
            "bfx-nonce": nonce,
            "bfx-apikey": self.__KEY,
            "bfx-signature": hexstring,
            "content-type": "application/json"
        }

    def req(self, path, params=None):
        if params is None:
            params = {}
        nonce = self._nonce()
        body = params
        raw_body = json.dumps(body)
        headers = self._headers(path, nonce, raw_body)
        url = self.BASE_URL + path
        resp = requests.post(url, headers=headers, data=raw_body, verify=True)
        return resp

    def active_orders(self):
        # Fetch active orders
        response = self.req('v2/auth/r/orders')
        if response.status_code == 200:
            return response.json()
        else:
            print('error, status_code = ', response.status_code)
            return ''

    def account_info(self):
        response = self.req('v2/auth/r/info/user')
        if response.status_code == 200:
            return response.json()
        else:
            print('error, status_code = ', response.status_code)
            return ''

    def submit_market_order(self, symbol: str, amount: str):
        # Amount of order (positive for buy, negative for sell)
        response = self.req('v2/auth/w/order/submit',
                            params={'type': 'EXCHANGE MARKET', 'symbol': symbol, 'amount': amount})
        if response.status_code == 200:
            return response.json()
        else:
            print('error, status_code = ', response.status_code)
            return ''

    def order_history(self, symbol: str, limit: int):
        # Amount of order (positive for buy, negative for sell)
        response = self.req(f'v2/auth/r/orders/{symbol}/hist', params={'limit': limit})
        if response.status_code == 200:
            return response.json()
        else:
            print('error, status_code = ', response.status_code)
            return ''

    def get_balance_available(self, symbol: str, direction: int):
        if direction == -1:
            rate = '1'
        else:
            try:
                symbol_ticker = symbol[1:]
                r = requests.get(f'https://api.bitfinex.com/v1/pubticker/{symbol_ticker}')
                data = r.json()
                rate = data['last_price']
            except Exception as e:
                print(e)
                return
        # dir -> Direction of the order (1 for by, -1 for sell)
        # rate-> rate is price you wanna buy or sell symbol , for sell is 1
        response = self.req('v2/auth/calc/order/avail',
                            params={'symbol': symbol, 'dir': direction, 'rate': rate, 'type': 'EXCHANGE'})
        if response.status_code == 200:
            return response.json()[0]
        else:
            print('error, status_code = ', response.status_code)
            print(response.text)
            return ''

    def get_assets(self):
        """
        :arg:
            None
        :return:
                [
                  [
                    WALLET_TYPE,
                    CURRENCY,
                    BALANCE,
                    UNSETTLED_INTEREST,
                    AVAILABLE_BALANCE,
                    LAST_CHANGE,
                    TRADE_DETAILS
                  ],
                  ...
                ]
        """
        response = self.req('v2/auth/r/wallets')
        if response.status_code == 200:
            return response.json()
        else:
            print('error, status_code = ', response.status_code)
            return ''