import shrimpy
import plotly.graph_objects as go

def initShrimp():
    shrimp_public_key = 'b6b6227c38f101d2041215a0594af3ec9d5befafc802db71e20ca46ca5f969fe'
    shrimp_secret_key = '25cce7c49ef74cf016916b9be1508b7e6dfcfd897032f62e1730d2e597fae8041a9fc690e63f1e7139557527662f678247ebd1e8ac18ae1d679a962963c1036f'
    api_client = shrimpy.ShrimpyApiClient(shrimp_public_key, shrimp_secret_key)
    return api_client

def createtrad():
    user_id = "ddc7222e-a7f0-47b6-ba7c-1d6fd20611c8"
    api_client=initShrimp()
    binance_public_key= 'Kjps274EHTI0f1Y2tY9F7TchaB8nbRZwbz5h5xvmQpD5HGrEJPN5loqjE32EQ9UP'
    binance_private_key= 'nC0TpFDobMjjstYjVVSdBccLLsm3ElKl35wk3zo4G9AGOpsqgxq67V5gDoNmtRnt'
    #link_account_response = api_client.link_account(user_id ,'binance' ,binance_public_key ,binance_private_key)
    trade=api_client.create_trade(user_id,151845,'BTC' ,'ETH' ,'0.01')
   # tradeStatus=api_client.get_trade_status(user_id,151845 ,trade['id'] )
    balance=api_client.get_balance(user_id,151845)
    print(balance)
def handler(msg):
    ticker = msg['content'][len(msg['content']) - 1]['price']
    print(ticker)
def error_handler(err):
    print(err)
def liveTicker():
    client=initShrimp()
    raw_token = client.get_token()
    client_toc = shrimpy.ShrimpyWsClient(error_handler, raw_token['token'])

    subscribe_data = {
        "type": "subscribe",
        "exchange": "binance",
        "pair": "btc-usdt",
        "channel": "trade"
    }
    client_toc.connect()
    client_toc.subscribe(subscribe_data ,handler)

def drawCandle():
    client = initShrimp()
    candles = client.get_candles(
        'binance',  # exchange
        'BTC',  # base_trading_symbol
        'USDT',  # quote_trading_symbol
        '1m'  # interval
    )
    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []

    for candle in candles:
        dates.append(candle['time'])
        open_data.append(candle['open'])
        high_data.append(candle['high'])
        low_data.append(candle['low'])
        close_data.append(candle['close'])

    fig = go.Figure(data=[go.Candlestick(x=dates,
                                         open=open_data, high=high_data,
                                         low=low_data, close=close_data)])
    fig.show()


def trad():
    client = initShrimp()
    id = client['account']
    print(id)


def getStatus():
    client = initShrimp()
    client.link_account()
    print(client)

