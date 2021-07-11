from demoAccount import *
from stream import AsWebSocketClient
from Analysis import *
from ML import NeuralNetwork
from test import Test
if __name__ == '__main__':
    api_key = 'Kjps274EHTI0f1Y2tY9F7TchaB8nbRZwbz5h5xvmQpD5HGrEJPN5loqjE32EQ9UP'
    api_secret = 'nC0TpFDobMjjstYjVVSdBccLLsm3ElKl35wk3zo4G9AGOpsqgxq67V5gDoNmtRnt'
    client = Account(balance=400 , name='mohamad' ,api_key=api_key ,api_secret=api_secret)
    # input timeframes {day  , 1hour , 1month  , 1week  , 1min  , 4hour ,  5min  ,  15min}
    data = client.get_data('BTCUSDT' , '1min')
    to_csv(data=data , name='new.csv')
    # test = Test(account=client )
    # test.bankAccount_with_coin_ideal(data=data , symbol='btc' , sell_amount=0.01 , buy_amount=0.01 )
    # test.bankAccount_with_coin_ichiCross(ichi_recomm=recom , prices=data , symbol='btc' , sell_amount=0.01 , buy_amount=0.01 )

    time = '{hour}:{minute}'.format(hour=5 , minute=45)

    training_outputs = get_detect(data=data , start_time=time)
    ichi = get_indicators_col(data).fillna(value=-1)
    recom = ichimoku_recommend(price_data=data, ichimoku=ichi)
    to_csv(data=recom, name='recomIchi.csv')
    training_inputs = recom_without_noidea(recom,time)
    # tr = TradingView(symbol="BTCUSDT" , time_frame="day" ,screener="crypto" , exchange="binance")
    neural_network = NeuralNetwork(element_number=10 )
    print("Beginning Randomly Generated Weights: ")
    print(neural_network.synaptic_weights)
    # training taking place
    neural_network.train(training_inputs, training_outputs, 10000)
    print("Ending Weights After Training: ")
    print(neural_network.synaptic_weights)
    # '1min''3min''5min''15min''30min''1hour''2hour''4hour''6hour''8hour''12hour''1day''3day''1week' '1month'
    websocket = AsWebSocketClient(client=client ,nn=neural_network, symbol='BTCUSDT' , time_frame='1min', time=time)
    websocket.live_realtime_price()

