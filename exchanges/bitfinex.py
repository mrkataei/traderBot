from .base import Exchange
import sys

def _nonce():
    # Returns a nonce
    # Used in authentication
    return str(int(round(time.time() * 10000)))


class Bitfinex(Exchange):
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
                return response.json()
            else:
                return False
        except Exception as e:
            return False
