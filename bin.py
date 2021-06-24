from binance.client import Client
from binance import  ThreadedWebsocketManager
import pyttsx3
import client as cl
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from datetime import datetime
import xlwt
from xlwt import Workbook
import numpy as np
api_key ='Kjps274EHTI0f1Y2tY9F7TchaB8nbRZwbz5h5xvmQpD5HGrEJPN5loqjE32EQ9UP'
api_secret ='nC0TpFDobMjjstYjVVSdBccLLsm3ElKl35wk3zo4G9AGOpsqgxq67V5gDoNmtRnt'

binanceUser = cl.ClientBinance(api_key , api_secret)
client = binanceUser.get_client()
candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE)

dates = []
open_data = []
high_data = []
low_data = []
vol =[]
close_data = []


for candle in candles:
    dates.append(datetime.fromtimestamp(int(candle[0])/1000))
    open_data.append(candle[1])
    high_data.append(candle[2])
    low_data.append(candle[3])
    close_data.append(candle[4])
    vol.append(float(candle[5]))
df = pd.DataFrame(close_data)
df2 = pd.DataFrame(vol)
df3 = pd.DataFrame(close_data)
df4 = pd.DataFrame(close_data)

# df2['volMA'] = df2.rolling(60).mean()
df2['volEMA60'] = df2.ewm(span=60).mean()
df['MA20'] = df.rolling(60).mean()
df3['EMA24'] = df3.ewm(span=24).mean()
df4['EMA12'] = df4.ewm(span=12).mean()



fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Candlestick(x=dates,open=open_data, high=high_data,low=low_data, close=close_data) , secondary_y=False)
# fig.add_trace(go.Scatter(x=dates, y=df.MA20, line=dict(color='orange', width=1)) ,secondary_y=False)
fig.add_trace(go.Scatter(x=dates, y=df3.EMA24, line=dict(color='green', width=1)) ,secondary_y=False)
fig.add_trace(go.Scatter(x=dates, y=df4.EMA12, line=dict(color='orange', width=1)) ,secondary_y=False)
fig.add_trace(go.Scatter(x=dates, y=vol, line=dict(color='blue', width=1)) ,secondary_y=True)
# fig.add_trace(go.Scatter(x=dates, y=df2.volMA, line=dict(color='orange', width=1)) ,secondary_y=True)
fig.add_trace(go.Scatter(x=dates, y=df2.volEMA60, line=dict(color='orange', width=1)) ,secondary_y=True)
# fig = go.Figure(data=[go.Candlestick(x=dates,
#                                          open=open_data, high=high_data,
#                                          low=low_data, close=close_data),
#                       go.Scatter(x=dates, y=df.MA20, line=dict(color='orange', width=1)),
#                       go.Scatter(x=dates, y=vol, line=dict(color='blue', width=1))])
# fig.update_layout(height=600, width=800, title_text="Side By Side Subplots")
fig.show()
malen=len(df.MA20)
cllen=len(close_data)

if df.MA20.iloc[malen-1] >= float(close_data[cllen-1]):
    pyttsx3.speak("sells your crypto" + "current price is" + close_data[420] + "and EMA is " +  str(df.MA20.iloc[422]))
    print("sell\n")
    print("current price is" + close_data[cllen-1] + "\n")
    print("and EMA is " +  str(df.MA20.iloc[malen-1]))
else:
    pyttsx3.speak("hold your crypto")
    print("hold your crypto")


#
# wb = Workbook()
# sheet1 = wb.add_sheet('Sheet 1')
# sheet1.write(0, 1, 'Open price')
# sheet1.write(0, 2, 'High price')
# sheet1.write(0, 3, 'Low price')
# sheet1.write(0, 4, 'Close price')
# sheet1.write(0, 5, 'Time')
#
# i = 1
# for candle in candles:
#     sheet1.write(i, 1,candle[1] )
#     sheet1.write(i, 2,candle[2] )
#     sheet1.write(i, 3,candle[3] )
#     sheet1.write(i, 4,candle[4] )
#     sheet1.write(i, 5,datetime.fromtimestamp(int(candle[0])/1000).strftime("%m/%d/%Y, %H:%M:%S") )
#     i = i + 1
#
# wb.save('prices4.xls')