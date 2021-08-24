from Telegram.Client import tele
import threading
from Analysis import stream


polling_thread = threading.Thread(target=tele.bot_polling)
polling_thread.daemon = True
polling_thread.start()

if __name__ == '__main__':
    stream.run()
