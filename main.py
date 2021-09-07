import threading
from Analysis.stream import StreamIchimoku
from Telegram.Client.tele import ClientBot
from Libraries.data_collector import generate_data
from time import sleep

generate_data('BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT', 'BCHUSDT', 'ETCUSDT')
client = ClientBot()
ichimoku_btcusdt = StreamIchimoku(symbol='BTCUSDT')
ichimoku_ethusdt = StreamIchimoku(symbol='ETHUSDT')

# client bot
polling_thread = threading.Thread(target=client.bot_polling)
polling_thread.daemon = True
polling_thread.start()

btcusdt_thread = threading.Thread(target=ichimoku_btcusdt.run)
btcusdt_thread.daemon = True
btcusdt_thread.start()

ethusdt_thread = threading.Thread(target=ichimoku_ethusdt.run)
ethusdt_thread.daemon = True
ethusdt_thread.start()

if __name__ == '__main__':
    while True:
        print("Running...")
        sleep(2000000)
