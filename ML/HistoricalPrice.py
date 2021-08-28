import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tensorflow.keras import *
from tensorflow.keras.layers import Bidirectional, LSTM, Dense, Activation


# based on https://towardsdatascience.com/the-beginning-of-a-deep-learning-trading-bot-part1-95-accuracy-
# is-not-enough-c338abc98fc2
def preprocess(data: pd.DataFrame):
    data['Date'] = pd.to_datetime(data['Date'])
    return data


def plot_historical(data: pd.DataFrame):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Candlestick(x=data['Date'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
        secondary_y=False)
    fig.show()


def create_model():
    model = Sequential()
    model.add(Bidirectional(LSTM(10, return_sequences=True), input_shape=(5, 10)))
    model.add(Bidirectional(LSTM(10)))
    model.add(Dense(5))
    model.add(Activation('softmax'))
    model.compile(loss="mse", optimizer="adam", metrics=['mae', 'mape'])
    return model


class BidirectionalLSTM:
    __data = None
    __train = None
    __valid = None
    __test = None
    __model = None

    def __init__(self, data: pd.DataFrame):
        self.__data = preprocess(data)
        self.__preprocess()
        self.__split()
        self.__model = create_model()

    def __preprocess(self):
        self.__data['Open'] = self.__data['Open'].pct_change()
        self.__data['High'] = self.__data['High'].pct_change()
        self.__data['Low'] = self.__data['Low'].pct_change()
        self.__data['Close'] = self.__data['Close'].pct_change()
        self.__data['Volume'] = self.__data['Volume'].pct_change()

        '''Normalize price columns'''
        min_return = min(self.__data[['Open', 'High', 'Low', 'Close']].min(axis=0))
        max_return = max(self.__data[['Open', 'High', 'Low', 'Close']].max(axis=0))

        # Min-max normalize price columns (0-1 range)
        self.__data['Open'] = (self.__data['Open'] - min_return) / (max_return - min_return)
        self.__data['High'] = (self.__data['High'] - min_return) / (max_return - min_return)
        self.__data['Low'] = (self.__data['Low'] - min_return) / (max_return - min_return)
        self.__data['Close'] = (self.__data['Close'] - min_return) / (max_return - min_return)

        '''Normalize volume column'''
        min_volume = self.__data['Volume'].min(axis=0)
        max_volume = self.__data['Volume'].max(axis=0)

        # Min-max normalize volume columns (0-1 range)
        self.__data['Volume'] = (self.__data['Volume'] - min_volume) / (max_volume - min_volume)
        print(self.__data)

    def __split(self):
        times = sorted(self.__data.index.values)
        last_10pct = sorted(self.__data.index.values)[-int(0.1 * len(times))]  # Last 10% of series
        last_20pct = sorted(self.__data.index.values)[-int(0.2 * len(times))]  # Last 20% of series

        self.__train = self.__data[(self.__data.index < last_20pct)]  # Training data are 80% of total data
        self.__valid = self.__data[(self.__data.index >= last_20pct) & (self.__data.index < last_10pct)]
        self.__test = self.__data[(self.__data.index >= last_10pct)]
