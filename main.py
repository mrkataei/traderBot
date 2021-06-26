from demoAccount import *
from stream import AsWebSocketClient


if __name__ == '__main__':
    api_key = 'Kjps274EHTI0f1Y2tY9F7TchaB8nbRZwbz5h5xvmQpD5HGrEJPN5loqjE32EQ9UP'
    api_secret = 'nC0TpFDobMjjstYjVVSdBccLLsm3ElKl35wk3zo4G9AGOpsqgxq67V5gDoNmtRnt'
    client = Account(balance=1000 , name='kourosh' ,api_key=api_key ,api_secret=api_secret)
    # input timeframes {day  , 1hour , 1month  , 1week  , 1min  , 4hour ,  5min  ,  15min}
    data = client.get_data('BTCUSDT' , '1min')
    print(client.get_detect())
    # data = data.fillna(value=0)
    websocket = AsWebSocketClient('BTCUSDT', data)
    # '1min''3min''5min''15min''30min''1hour''2hour''4hour''6hour''8hour''12hour''1day''3day''1week' '1month'
    websocket.live_realtime_price(time_frame='1min')
    # tr = TradingView(symbol="BTCUSDT" , time_frame="day" ,screener="crypto" , exchange="binance")
    # initializing the neuron class
    # neural_network = NeuralNetwork()
    # print("Beginning Randomly Generated Weights: ")
    # print(neural_network.synaptic_weights)
    # training data consisting of 4 examples--3 input values and 1 output
    # training_inputs = np.array([[0, 0, 0 , 0],
    #                             [1, 1, 1 , 0],
    #                             [1, 0, 1 , 0],
    #                             [0, 1, 1 , 1],
    #                             [0, 0 ,0,  0]])
    # training_outputs = np.array([[1, 1, 1, 1, 1]]).T

    # training taking place
    # neural_network.train(training_inputs, training_outputs, 115000)
    #
    # print("Ending Weights After Training: ")
    # print(neural_network.synaptic_weights)
    # while True:
    #     user_input_one = str(input("User Input One: "))
    #     user_input_two = str(input("User Input Two: "))
    #     user_input_three = str(input("User Input Three: "))
    #     user_input_four = str(input("User Input four: "))
    #     print("Considering New Situation: ", user_input_one, user_input_two, user_input_three ,user_input_four)
    #     print("New Output data: ")
    #     print(neural_network.think(np.array([user_input_one, user_input_two, user_input_three ,user_input_four])))
    #     print("Wow, we did it!")
