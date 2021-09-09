import threading
from Analysis.stream import run_ichimoku_threads
from Telegram.Client.tele import ClientBot
from Libraries.data_collector import generate_data
from time import sleep

generate_data('BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT', 'BCHUSDT', 'ETCUSDT')
client = ClientBot()
# client bot
polling_thread = threading.Thread(target=client.bot_polling)
polling_thread.daemon = True
polling_thread.start()

ichimoku_thread = threading.Thread(target=run_ichimoku_threads, args=('BTCUSDT', 'ETHUSDT', 'ADAUSDT',
                                                                      'DOGEUSDT', 'BCHUSDT', 'ETCUSDT'))
ichimoku_thread.daemon = True
ichimoku_thread.start()

if __name__ == '__main__':
    while True:
        print("Running...")
        sleep(2000000)
