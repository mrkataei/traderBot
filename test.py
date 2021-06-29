from demoAccount import Account
import pandas as pd
class Test:
  __account = None
  def __init__(self , account:Account):
      self.__account = account
  def bankAccount_with_coin_ideal(self ,data:pd.DataFrame ,  symbol:str ,sell_amount:float, buy_amount:float):
      last_detect = 0 if self.__account.get_coins_amount('btc') == 0 else 1
      for price, detect in zip(data.close, data.detect):
          if last_detect != detect:
              if detect == 1:
                  self.__account.coin_exchange(symbol=symbol, amount=buy_amount, buy=True, price=float(price))
              else:
                  self.__account.coin_exchange(symbol=symbol, amount=sell_amount, buy=False, price=float(price))
              last_detect = detect
          else:
              continue

      self.__account.export_to_excel('transaction')
