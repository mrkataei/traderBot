from demoAccount import Account
import pandas as pd
class Test:
    __account = None
    __last_detect = None
    def __init__(self , account:Account):
        self.__account = account
        self.__last_detect = 0 if self.__account.get_coins_amount('btc') == 0 else 1
    def bankAccount_with_coin_ideal(self ,data:pd.DataFrame ,  symbol:str ,sell_amount:float, buy_amount:float):
        for price, detect in zip(data.close, data.detect):
            if self.__last_detect  != detect:
                if detect == 1:
                    self.__account.coin_exchange(symbol=symbol, amount=buy_amount, buy=True, price=float(price))
                else:
                    self.__account.coin_exchange(symbol=symbol, amount=sell_amount, buy=False, price=float(price))
                self.__last_detect  = detect
            else:
                continue

        self.__account.export_to_excel('transaction')

    def bankAccount_with_coin_ichiCross(self ,ichi_recomm:pd.DataFrame,prices:pd.DataFrame ,  symbol:str ,sell_amount:float, buy_amount:float):
        data = pd.DataFrame()
        data['kijunAndSpanBCross'] = ichi_recomm['kijunAndSpanBCross']
        data['close'] = prices['close']
        print(data)

        for price, detect in zip(data.close, data.kijunAndSpanBCross):
            if detect != -1 and self.__last_detect  != detect:
                if detect == 1:
                    self.__account.coin_exchange(symbol=symbol, amount=buy_amount, buy=True, price=float(price))
                else:
                    self.__account.coin_exchange(symbol=symbol, amount=sell_amount, buy=False, price=float(price))
                self.__last_detect  = detect
            else:
                continue


        self.__account.export_to_excel('transaction')