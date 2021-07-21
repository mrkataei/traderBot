# from Account.demoAccount import *
# from Analysis.Analysis import *
# from ML.ML import BasicNeuralNetwork
# from stream import AsWebSocketClient
import pandas as pd
from ML.HistoricalPrice import BidirectionalLSTM

if __name__ == '__main__':

    data = pd.read_csv('Static/IBM.csv')
    test = BidirectionalLSTM(data=data)
    test.plot_historical()
    # api_key = 'Kjps274EHTI0f1Y2tY9F7TchaB8nbRZwbz5h5xvmQpD5HGrEJPN5loqjE32EQ9UP'
    # api_secret = 'nC0TpFDobMjjstYjVVSdBccLLsm3ElKl35wk3zo4G9AGOpsqgxq67V5gDoNmtRnt'
    # client = Account(balance=400 , name='mohamad' ,api_key=api_key ,api_secret=api_secret)
    # # input timeframes {day  , 1hour , 1month  , 1week  , 1min  , 4hour ,  5min  ,  15min}
    # data = client.get_data('BTCUSDT' , '1min')
    # to_csv(data=data , name='Static/data.csv')
    #
    # #for test data by detect value or indicators value
    # # test = Test(account=client )
    # # test.bankAccount_with_coin_ideal(data=data , symbol='btc' , sell_amount=0.01 , buy_amount=0.01 )
    # # test.bankAccount_with_coin_ichiCross(ichi_recomm=recom , prices=data , symbol='btc' , sell_amount=0.01 , buy_amount=0.01 )
    #
    # #get data from asset and clean and preprocess
    # # data = pd.read_csv('Static/BTCUSDT.csv')
    # # data['detect'] = data['detect'].astype(int)
    #
    # #if get data from asset your need this drop line
    # # recom.drop(recom.head(80).index, inplace=True)
    # # data.drop(data.head(80).index, inplace=True)
    #
    # #for now watch recommendation data from Ichimoku and choose time format like line bellow which dont have any -1
    # time = '05:52'
    # training_outputs = get_detect(data= data, start_time=time)
    # #fill rows which have no ideas values indicators by -1
    # ichimoku = get_indicators_col(data).fillna(value=-1)
    # recommendation = ichimoku_recommend(price_data=data, ichimoku=ichimoku)
    #
    # #save recommendation for watch time and data to csv
    # to_csv(data=recommendation, name='Static/recommendation_ichimoku.csv')
    # #return training inputs from ichimoku recommendation with numpy array
    # training_inputs = recom_without_noidea(recommendation, time)
    # #trading view class for analysis and recommendation
    # # tr = TradingView(symbol="BTCUSDT" , time_frame="day" ,screener="crypto" , exchange="binance")
    # neural_network = BasicNeuralNetwork(element_number=10)
    # print("Beginning Randomly Generated Weights: ")
    # print(neural_network.synaptic_weights)
    # # training taking place
    # neural_network.train(training_inputs, training_outputs, 10000)
    # print("Ending Weights After Training: ")
    # print(neural_network.synaptic_weights)
    # # '1min''3min''5min''15min''30min''1hour''2hour''4hour''6hour''8hour''12hour''1day''3day''1week' '1month'
    # websocket = AsWebSocketClient(client=client ,nn=neural_network, symbol='BTCUSDT' , time_frame='1min', time=time)
    # websocket.live_realtime_price()
