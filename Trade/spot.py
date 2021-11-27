"""
    Mr.Kataei 11/12/2021
    need risk profile for users - this work just for Aran account
"""

from Account.clients import BitfinexClient


class BitfinexSpot(BitfinexClient):
    def __init__(self, public: str, secret: str):
        BitfinexClient.__init__(self, public=public, secret=secret)

    def buy_market(self, symbol: str, percent: float):
        amount = self.get_balance_available(symbol=symbol, direction=1)
        amount = amount * percent
        result = self.submit_market_order(symbol=symbol, amount=str(amount))
        return result

    def sell_market(self, symbol: str, percent: float):
        amount = self.get_balance_available(symbol=symbol, direction=-1)
        amount = amount * percent
        result = self.submit_market_order(symbol=symbol, amount=str(amount))
        return result

