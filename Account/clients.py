"""
Mr.Kataei 8/4/2021
use for telegram bot to register and login and logout
"""
import hashlib
import hmac
import json
import time

import requests


class User:
    def __init__(self):
        self.username = None
        self.session = False
        self.watchlist = []
        self.temp_watch = None
        self.coin = None
        self.analysis = None
        self.timeframe = None
        self.temp = None
        self.login = False


class Register:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.username: str
        self.password1: str
        self.password2: str
        self.security_question_id: int
        self.security_question: str
        self.security_answer: str


class BitfinexClient:
    BASE_URL = "https://api.bitfinex.com/"
    __KEY = "KeRPcVqCQQw37SekGlPf37Am6DhzdCeqHBfgyieNNra"
    __SECRET = "b2pYpIXMdfpZgP0F8sXWiWRgcrkHNY6BmnfMtYe7BsI"

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

    def submit_limit_order(self, symbol: str, price: str, amount: str):
        # Amount of order (positive for buy, negative for sell)
        response = self.req('v2/auth/w/order/submit',
                            params={'type': 'LIMIT', 'symbol': symbol, 'price': price, 'amount': amount, 'lev': 1})
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

