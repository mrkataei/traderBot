from Analysis.stream import run_ichimoku_threads
from Libraries.data_collector import generate_data
from time import sleep
generate_data('BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT', 'BCHUSDT', 'ETCUSDT')

if __name__ == '__main__':
    run_ichimoku_threads('BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT', 'BCHUSDT', 'ETCUSDT')
    while True:
        print("Running...")
        sleep(2000000)
