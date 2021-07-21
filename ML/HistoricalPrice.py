import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def preprocess(data:pd.DataFrame):
    data['Date'] = pd.to_datetime(data['Date'])
    return data


class BidirectionalLSTM:
    __data = None
    def __init__(self , data:pd.DataFrame ):
        self.__data = preprocess(data)
    def plot_historical(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Candlestick(x=self.__data['Date'], open=self.__data['Open'], high=self.__data['High'], low=self.__data['Low'], close=self.__data['Close']),
                      secondary_y=False)
        fig.show()

