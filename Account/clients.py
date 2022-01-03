"""
Mr.Kataei 8/4/2021
use for telegram bot to register
and exchanges account implement here
"""
import hashlib
import hmac
import json
import sys
import time
import requests
from Interfaces.exchange import Exchange
from Inc import functions


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.username = None
        self.strategy = None
        self.account = None
        self.lang = 'en'

    def update_user_plan_limit(self):
        if self.username is not None:
            plan_id = functions.get_user_plan(username=self.username)
            plan = functions.record_dictionary(record=functions.get_plans(plan_id=plan_id)[0], table='plans')
            self.strategy = plan['strategy_number']
            self.account = plan['account_number']


class BitfinexClient(Exchange):
    BASE_URL = "https://api.bitfinex.com/"

    def __init__(self, public: str, secret: str):
        Exchange.__init__(self, public=public, secret=secret)

    def _nonce(self):
        # Returns a nonce
        # Used in authentication
        return str(int(round(time.time() * 10000)))

    def _headers(self, path, nonce, body):
        secbytes = self.SECRET.encode(encoding='UTF-8')
        signature = "/api/" + path + nonce + body
        sigbytes = signature.encode(encoding='UTF-8')
        h = hmac.new(secbytes, sigbytes, hashlib.sha384)
        hexstring = h.hexdigest()
        return {
            "bfx-nonce": nonce,
            "bfx-apikey": self.KEY,
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
            return False, response.json()
        else:
            return True, 'error, status_code = ' + str(response.status_code)

    def buy_market(self, symbol: str, percent: float):
        error, amount = self.get_balance_available(symbol=symbol, direction=1)
        if not error:
            amount = amount * percent/100
            error, result = self.submit_market_order(symbol=symbol, amount=str(amount))
            if not error:
                result = {'amount': result[4][0][7], 'order_status': result[4][0][13],
                          'order_submit_time': result[4][0][4], 'price': result[4][0][16],
                          'status': result[6]}
            return error, result
        else:
            return error, amount

    def sell_market(self, symbol: str, amount: float = sys.float_info.max):
        error, available_amount = self.get_balance_available(symbol=symbol, direction=-1)
        amount = - amount
        if not error:
            # sell all available amount if perv amount save db not available
            if amount < available_amount:
                amount = available_amount

            amount = amount * 0.999999
            error, result = self.submit_market_order(symbol=symbol, amount=str(amount))
            if not error:
                result = {'amount': result[4][0][7], 'order_status': result[4][0][13],
                          'order_submit_time': result[4][0][4], 'price': result[4][0][16],
                          'status': result[6]}
            return error, result
        else:
            return error, available_amount

    def order_history(self, symbol: str, limit: int):
        # Amount of order (positive for buy, negative for sell)
        response = self.req(f'v2/auth/r/orders/{symbol}/hist', params={'limit': limit})
        if response.status_code == 200:
            return False, response.json()
        else:
            return True, 'error, status_code = ' + str(response.status_code) + str(response.json)

    def get_balance_available(self, symbol: str, direction: int):
        try:
            symbol_ticker = symbol[1:]
            r = requests.get(f'https://api.bitfinex.com/v1/pubticker/{symbol_ticker}')
            data = r.json()
            rate = data['last_price']
        except Exception as e:
            return True, e
        # dir -> Direction of the order (1 for by, -1 for sell)
        # rate-> rate is price you wanna buy or sell symbol
        response = self.req('v2/auth/calc/order/avail',
                            params={'symbol': symbol, 'dir': direction, 'rate': rate, 'type': 'EXCHANGE'})
        if response.status_code == 200:
            return False, response.json()[0]
        else:
            return True, 'error = ' + response.text + ',status_code = ' + str(response.status_code)

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
            return None


class DemoClient(Exchange):
    def __init__(self, chat_id: str):
        Exchange.__init__(self, public='public', secret='secret')
        self.chat_id = chat_id

    def submit_market_order(self, symbol: str, amount: str):
        print()

    def get_balance_available(self, symbol: str, direction: int):
        print()

    def buy_market(self, symbol: str, percent: float):
        print()

    def sell_market(self, symbol: str, percent: float):
        print()

    def get_assets(self):
        assets = functions.get_demo_account_assets(chat_id=self.chat_id)
        if assets is not None:
            assets = assets[0]
            assets = [['exchange', 'BTC', assets[0]], ['exchange', 'ETH', assets[1]], ['exchange', 'BCH', assets[2]],
                      ['exchange', 'ETC', assets[3]], ['exchange', 'ADA', assets[4]], ['exchange', 'DOGE', assets[5]],
                      ['exchange', 'USDT', assets[5]]]

        return assets


class Nobitex(Exchange):
    def __init__(self, public: str, secret: str):
        Exchange.__init__(self, public=public, secret=secret)

    def submit_market_order(self, symbol: str, amount: str):
        print()

    def get_balance_available(self, symbol: str, direction: int):
        print()

    def buy_market(self, symbol: str, percent: float):
        print()

    def sell_market(self, symbol: str, percent: float):
        print()

    def get_assets(self):
        print()




