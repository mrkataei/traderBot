from .base import Exchange


class Demo(Exchange):
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
