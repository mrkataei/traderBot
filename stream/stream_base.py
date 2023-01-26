import threading
import datetime
from time import sleep, time, process_time
# from strategies.base import Strategy
class Stream:
    def __init__(self, check_time: float):
        self.check_time = check_time
        # self.strategy = strategy

    def check(self, func):
        while True:
            func()
            sleep(self.check_time)
                    # data = candles(symbol=self.symbol, number=15, unit='m', limit=400)
                    # if data[0]:
                    #     ruby = Ruby(data=data[1], coin_id=self.coin_id, timeframe_id=6, bot_ins=_bot_ins)
                    #     ruby.signal()
                    # delay = process_time()

    def run(self):
        check = threading.Thread(target=self.check)
        check.start()

def hello():
    print('injas')

Stream(check_time=5).check(func=hello)

print('salam')
                # sleep(abs(900 - delay))

# threading.Thread(target=hello).start()
    
