from Telegram import tele
import threading
from time import sleep



polling_thread = threading.Thread(target=tele.bot_polling)
polling_thread.daemon = True
polling_thread.start()


if __name__ == '__main__':

    while True:
        try:
            print()
            sleep(20)
        except KeyboardInterrupt:
            break
