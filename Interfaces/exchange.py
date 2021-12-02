class Exchange:
    def __init__(self, public: str, secret: str):
        self.KEY = public
        self.SECRET = secret

    def submit_market_order(self, symbol: str, amount: str):
        raise Exception("NotImplementedException")

    def get_balance_available(self, symbol: str, direction: int):
        raise Exception("NotImplementedException")

    def buy_market(self, symbol: str, percent: float):
        raise Exception("NotImplementedException")

    def sell_market(self, symbol: str, percent: float):
        raise Exception("NotImplementedException")

    def get_assets(self):
        raise Exception("NotImplementedException")
