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
    # data = cast_to_float(data).fillna(value=-1)
    #
    # data = cast_to_float(data).fillna(value=-1)
    time = '05:20'
    training_outputs = client.get_detect(time)
    # print(training_outputs)
    # inputs = np.array([[0, 0, 0, 0],
    #                             [1, 1, 1 , 0],
    #                             [1, 0, 1 , 0],
    #                             [0, 1, 1 , 1],
    #                             [0, 0 ,0,  0]])
    # print(inputs)
    ichi = get_indicators_col(data).fillna(value=-1)
    recom = ichimoku_recommend(price_data=data, ichimoku=ichi)
    training_inputs = recom_without_noidea(recom,time)


    # print(training_inputs)
    # print(np.array(recom).astype(int))
    # recom_without_noidea(recom , )
    # test.bankAccount_with_coin_ichiCross(ichi_recomm=recom , prices=data , symbol='btc' , sell_amount=0.01 , buy_amount=0.01 )
    # to_csv(data=recom, name='recomlchi.csv')
    # data = data.fillna(value=0)
    # detect = client.get_detect(start_time='03:21:00')
    # print(detect)
    # websocket = AsWebSocketClient('BTCUSDT', data)
    # '1min''3min''5min''15min''30min''1hour''2hour''4hour''6hour''8hour''12hour''1day''3day''1week' '1month'
    # websocket.live_realtime_price(time_frame='1min')

    # tr = TradingView(symbol="BTCUSDT" , time_frame="day" ,screener="crypto" , exchange="binance")
    # initializing the neuron class
    neural_network = NeuralNetwork(element_number=10 )
    print("Beginning Randomly Generated Weights: ")
    print(neural_network.synaptic_weights)
    # training data consisting of 4 examples--3 input values and 1 output
    # training_inputs = np.array([[0, 0, 0 , 0 ,0, 0, 0 , 0, 0, 0 ],
    #                             [1, 1,0, 0, 0 , 0, 0, 0, 1 , 0],
    #                             [1, 0, 1 ,0, 0, 0 , 0, 0, 0 , 0],
    #                             [0, 1,0, 0, 0 , 0, 0, 0 , 1 , 1],
    #                             [0,0, 0, 0 , 0, 0, 0 , 0 ,0,  0]])
    # print(len(training_inputs))
    # print(training_inputs)
    # training_outputs = np.array([[1, 1, 1, 1, 1]]).T
    # print(len(training_outputs))
    # print(training_outputs)


    # training taking place
    neural_network.train(training_inputs, training_outputs, 100)
    #
    print("Ending Weights After Training: ")
    print(neural_network.synaptic_weights)
    while True:
        user_input_one = str(input("User Input One: "))
        user_input_two = str(input("User Input Two: "))
        user_input_three = str(input("User Input Three: "))
        user_input_four = str(input("User Input four: "))
        user_input_five = str(input("User Input five: "))
        user_input_six = str(input("User Input six: "))
        user_input_seven = str(input("User Input seven: "))
        user_input_eight = str(input("User Input eight: "))
        user_input_nine = str(input("User Input nine: "))
        user_input_ten = str(input("User Input ten: "))
        print("Considering New Situation: ", user_input_one, user_input_two, user_input_three ,user_input_four ,user_input_five , user_input_six , user_input_seven , user_input_eitgh , user_input_nine , user_input_ten)
        print("New Output data: ")
        print(neural_network.think(np.array([user_input_one, user_input_two, user_input_three ,user_input_four,user_input_five , user_input_six , user_input_seven , user_input_eitgh , user_input_nine , user_input_ten])))
        print("Wow, we did it!")
