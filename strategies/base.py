"""
    Mr.Kataei 11/12/2021

"""
from datetime import datetime
import pandas as pd
from Inc.functions import get_last_recommendations, set_recommendation, record_dictionary
from trade.spot import submit_order
from telegram.Client.message import broadcast_messages


class Strategy:
    def __init__(self, data: pd.DataFrame, coin_id: int, timeframe_id: int, analysis_id: int, bot_ins):
        """
            :param data: OHCL dataframe
            :param coin_id: { 1:BTCUSDT, 2:ETHUSDT, 3:ADAUSDT, 4:ETCUSDT, 5:BCHUSDT, 6:DOGEUSDT}
            :param timeframe_id:{ 1:30min, 2:1hour, 3:4hour, 4:1day, 5:1min}
            :param analysis_id: { 1:emerald , 2:ruby, 3:diamond }
            :param bot_ins: it's instance of telegram bot obj, for broadcast signals

        """
        self.data = data
        self.coin_id = coin_id
        self.timeframe_id = timeframe_id
        self.analysis_id = analysis_id
        self.bot = bot_ins
        self.time = datetime.now()
        self.data['recommendation'] = None
        self.data['risk'] = None
        self.last_position = self.get_last_position()
        self.last_price = self.get_last_price()

    def get_source(self, source: str = 'close'):
        """
        :param source:
        :return:
        """
        return {
            'hl2': self.data.ta.hl2(),
            'hlc3': self.data.ta.hlc3(),
            'ohlc4': self.data.ta.ohlc4(),
            'close': self.data['close'],
            'high': self.data['high'],
            'low': self.data['low'],
            'open': self.data['open']
        }.get(source, self.data['close'])

    def get_last_position(self):
        """
            get last price(close) of analysis id
            old position by default is 'sell'
            :return: last pos
        """
        record = get_last_recommendations(analysis_id=self.analysis_id, timeframe_id=self.timeframe_id,
                                          coin_id=self.coin_id)
        if record:
            record = record[0]
            last_position = record_dictionary(record=record, table='recommendations')['position']
        else:
            last_position = 'sell'
        return last_position

    def get_last_price(self):
        """
            get last price(close) of analysis id
            old position by default is '0'
            :return: last_price
        """
        query = get_last_recommendations(analysis_id=self.analysis_id, timeframe_id=self.timeframe_id,
                                         coin_id=self.coin_id)
        if query:
            last_price = record_dictionary(query[0], "recommendations")["price"]
        else:
            last_price = 0
        return last_price

    def insert_database(self, position: str, current_price: float, risk: str):
        set_recommendation(analysis_id=self.analysis_id, coin_id=self.coin_id, timeframe_id=self.timeframe_id,
                           position=position, risk=risk, price=current_price)

    def broadcast(self, position: str, current_price: float, risk: str):
        broadcast_messages(coin_id=self.coin_id, analysis_id=self.analysis_id, timeframe_id=self.timeframe_id,
                           position=position, current_price=current_price, risk=risk, bot_ins=self.bot)

    def buy(self):
        submit_order(coin_id=self.coin_id, analysis_id=self.analysis_id, position='buy',
                     time_receive_signal=self.time)

    def sell(self):
        submit_order(coin_id=self.coin_id, analysis_id=self.analysis_id, position='sell',
                     time_receive_signal=self.time)

    def order(self, position: str):
        if position == 'buy':
            self.buy()
        elif position == 'sell':
            self.sell()

    def _set_recommendation(self, position: str, risk: str, index):
        # set recommendation and risk in dataframe
        self.data.loc[index, 'recommendation'] = position
        self.data.loc[index, 'risk'] = risk

    def get_recommendations(self):
        """
            apply signal to dataframe
            and add risk and recommendation column to dataframe
            :return: dataframe
        """
        self.signal_detector()
        return self.data[['date', 'open', 'high', 'close', 'low', 'risk', 'recommendation']].copy()

    def signal_detector(self):
        self.data.apply(lambda row: self.logic(row), axis=1)

    def preprocess(self):
        raise Exception("NotImplementedException")

    def logic(self, row):
        """
            check a row of dataframe to check diamond conditions and insert position to recommendation
             column and risk to risk column
            :param row: a row of dataframe
        """
        raise Exception("NotImplementedException")

    def signal(self):
        """
            check last row of processed dataframe to generate signal
        """
        last_row_detector = self.get_recommendations().tail(1)
        position = last_row_detector['recommendation'].values[0]
        if self.last_position != position and position is not None:
            close = float(last_row_detector['close'].values[0])

            self.broadcast(position=position, current_price=close, risk=last_row_detector['risk'].values[0])
            self.insert_database(position=position, current_price=close,
                                 risk=last_row_detector['risk'].values[0])
            self.order(position=position)

