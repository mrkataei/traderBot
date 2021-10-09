from Analysis.stream import StrategiesThreads
from Libraries.data_collector import generate_data
from time import sleep

generate_data()
thread = StrategiesThreads('BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT', 'BCHUSDT', 'ETCUSDT')

if __name__ == '__main__':
    thread.start_threads()
    while True:
        print("Running...")
        sleep(2000000)
