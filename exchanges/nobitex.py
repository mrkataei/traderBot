from .base import Exchange
import sys

def _nonce():
    # Returns a nonce
    # Used in authentication
    return str(int(round(time.time() * 10000)))


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
