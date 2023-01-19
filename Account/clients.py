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
import pandas as pd
import requests
from Interfaces.exchange import Exchange
from Inc import functions


class User:
    def __init__(self, message):
        self.chat_id = message.chat.id
        self.username = None
        self.strategy = None
        self.account = None
        self.lang ="fa"

    def update_user_plan_limit(self):
        if self.username is not None:
            plan_id = functions.get_user_plan(username=self.username)
            plan = functions.record_dictionary(record=functions.get_plans(plan_id=plan_id)[0], table='plans')
            self.strategy = plan['strategy_number']
            self.account = plan['account_number']


def _nonce():
    # Returns a nonce
    # Used in authentication
    return str(int(round(time.time() * 10000)))


class BitfinexClient(Exchange):
    BASE_URL = "https://api.bitfinex.com/"

    def __init__(self, public: str, secret: str):
        Exchange.__init__(self, public=public, secret=secret)
        self.fee = 0.003
        self.symbols = {'tETHUST': 'ETH', 'tBTCUST': 'BTC', 'tADAUST': 'ADA', 'tDOGE:UST': 'DOGE',
                        'tBCHN:UST': 'BCHN', 'tETCUST': 'ETC'}


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
        nonce = _nonce()
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
            amount = amount * percent / 100
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
        assets = self.get_assets()
        try:
            if not assets[0]:
                assets = assets[1]
            else:
                return True, assets[1]
            if direction == 1:
                usd = 0
                for asset in assets:
                    if 'UST' in asset:
                        usd = asset[2]
                r = requests.get(f'https://api-pub.bitfinex.com/v2/ticker/{symbol}')
                data = r.json()
                rate = data[6]
                if usd == 0:
                    return True, "not enough money"
                else:
                    return False, (float(usd) * (1 - self.fee)) / float(rate)
            elif direction == -1:
                amount = None
                for asset in assets:
                    if self.symbols[symbol] in asset:
                        amount = asset[2]
                if amount is not None:
                    return False, - float(amount)
                else:
                    return True, "no amount for sell"
        except Exception as e:
            return True, e

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
        try:
            response = self.req('v2/auth/r/wallets')
            if response.status_code == 200:
                return False, response.json()
            else:
                return True, response.status_code
        except Exception as e:
            return True, e


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

            return False, assets
        else:
            return True, 'error'


class Nobitex(Exchange):
    BASE_URL = "https://api.nobitex.ir/"

    def __init__(self, public: str, secret: str):
        Exchange.__init__(self, public=public, secret=secret)
        self.fee = 0.003
        self.symbols = {'ETHUSDT': 'ETH', 'BTCUSDT': 'BTC', 'BCHUSDT': 'BCH', 'ETCUSDT': 'ETC', 'DOGEUSDT': 'DOGE',
                        'ADAUSDT': 'ADA'}

    def _headers(self):
        return {
            "Authorization": f"Token {self.KEY}"
        }

    def req(self, path, params=None):
        if params is None:
            params = {}
        body = params
        raw_body = json.dumps(body)
        headers = self._headers()
        url = self.BASE_URL + path
        resp = requests.post(url, headers=headers, data=raw_body, verify=True)
        return resp

    def submit_market_order(self, symbol: str, amount: str):
        srcCurrency = self.symbols[symbol].lower()
        try:
            if float(amount) > 0:
                response = self.req('market/orders/add', params={'type': 'buy',
                                                                 "srcCurrency": srcCurrency, "dstCurrency": "usdt",
                                                                 "amount": amount,
                                                                 "execution": "market"})
            else:
                response = self.req('market/orders/add', params={"type": "sell",
                                                                 "srcCurrency": srcCurrency, "dstCurrency": "usdt",
                                                                 "amount": -float(amount),
                                                                 "execution": "market"})
            if response.status_code == 200:
                return False, response.json()
            else:
                return True, response.status_code
        except Exception as e:
            return True, None

    def get_balance_available(self, symbol: str, direction: int):
        assets = self.get_assets()
        symbol = self.symbols[symbol]
        try:
            if not assets[0]:
                assets = assets[1]
            else:
                return
            if direction == 1:
                usd = 0
                for asset in assets:
                    if 'USDT' in asset:
                        usd = float(asset[2])

                response = self.req('market/stats')
                if response.status_code == 200:
                    rate = response.json()['global']['binance'][symbol.lower()]
                else:
                    return False, response.status_code
                if usd == 0:
                    return True, "not enough money"
                else:
                    return False, (usd * (1 - self.fee)) / float(rate)
            elif direction == -1:
                amount = 0
                for asset in assets:
                    if symbol in asset:
                        amount = float(asset[2])
                if amount > 0:
                    return False, - amount
                else:
                    return True, "no amount for sell"
        except Exception as e:
            return True, e

    def buy_market(self, symbol: str, percent: float):
        error, amount = self.get_balance_available(symbol=symbol, direction=1)
        if not error:
            amount = amount * percent / 100
            error, result = self.submit_market_order(symbol=symbol, amount=str(amount))
            if not error:
                order = result['order']
                status = result['status']
                result = {'amount': str(order['amount']), 'order_status': order['status'],
                          'order_submit_time': time.time() * 1000, 'price': 0.0,
                          'status': status}
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
            error, result = self.submit_market_order(symbol=symbol, amount=str(amount))
            if not error:
                status = result['status']
                if status == "ok":
                    order = result['order']
                    result = {'amount': str(order['amount']), 'order_status': order['status'],
                              'order_submit_time': time.time() * 1000, 'price': 0.0,
                              'status': status}
                elif status == "failed":
                    result = result['message']
                    error = True
            return error, result
        else:
            return error, available_amount

    def get_assets(self):
        try:
            response = self.req('v2/wallets')
            if response.status_code == 200:
                assets = response.json()['wallets']
                assets = [['exchange', 'BTC', assets['BTC']['balance']], ['exchange', 'ETH', assets['ETH']['balance']],
                          ['exchange', 'BCH', assets['BCH']['balance']],
                          ['exchange', 'ETC', assets['ETC']['balance']], ['exchange', 'ADA', assets['ADA']['balance']],
                          ['exchange', 'DOGE', assets['DOGE']['balance']],
                          ['exchange', 'USDT', assets['USDT']['balance']]]
                return False, assets
            else:
                return True, response.status_code
        except Exception as e:
            return True, e

    def global_stats(self, symbol: str = None):
        try:
            response = self.req('market/global-stats')
            if response.status_code == 200:
                assets = response.json()
                markets = assets['markets']
                if symbol is None:
                    assets = pd.DataFrame(markets)
                else:
                    assets = markets['binance'][symbol]
                return False, assets
            else:
                return True, response.status_code
        except Exception as e:
            return True, e

    def last_price(self, srcCurrency: str, dstCurrency: str = 'usdt'):
        try:
            response = self.req('market/stats', params={"srcCurrency": srcCurrency,
                                                        "dstCurrency": dstCurrency})
            if response.status_code == 200:
                assets = response.json()
                return False, assets['global']['binance'][srcCurrency]
        except Exception as e:
            return True, e
