"""
Mr.Kataei 8/4/2021
for test analysis works truth we need test with demo account , this is have 2 functions for now
1- bankAccount_with_coin_ideal which trades base on detect analysis and buy or sell with coins already user have
2-bankAccount_with_coin_ichiCross in Analysis.py we have one strategy that name is ichi cross this method buy and sell
with this signal
any test with other signals must be implement here
"""
from Account.demo_account import Demo
import pandas as pd


class Test:
    __account = None
    __last_detect = None

    def __init__(self, account: Demo):
        self.__account = account
        self.__last_detect = 0 if self.__account.get_coins_amount('btc') == 0 else 1

    def bank_account_with_coin_ideal(self, data: pd.DataFrame, symbol: str, sell_amount: float, buy_amount: float):
        for price, detect in zip(data.close, data.detect):
            if self.__last_detect != detect:
                if detect == 1:
                    self.__account.coin_exchange(symbol=symbol, amount=buy_amount, buy=True, price=float(price))
                else:
                    self.__account.coin_exchange(symbol=symbol, amount=sell_amount, buy=False, price=float(price))
                self.__last_detect = detect
            else:
                continue

        self.__account.export_to_excel('transaction')

    def bank_account_with_coin_ichi_cross(self, ichi_recomm: pd.DataFrame, prices: pd.DataFrame, symbol: str,
                                          sell_amount: float, buy_amount: float):
        data = pd.DataFrame()
        data['kijunAndSpanBCross'] = ichi_recomm['kijunAndSpanBCross']
        data['close'] = prices['close']
        print(data)

        for price, detect in zip(data.close, data.kijunAndSpanBCross):
            if detect != -1 and self.__last_detect != detect:
                if detect == 1:
                    self.__account.coin_exchange(symbol=symbol, amount=buy_amount, buy=True, price=float(price))
                else:
                    self.__account.coin_exchange(symbol=symbol, amount=sell_amount, buy=False, price=float(price))
                self.__last_detect = detect
            else:
                continue

        self.__account.export_to_excel('transaction')
