from Telegram import tele
import threading
from time import sleep
import asyncio
from Analysis import ichimoku


polling_thread = threading.Thread(target=tele.bot_polling)
polling_thread.daemon = True
polling_thread.start()

if __name__ == '__main__':
    while True:
        print("connected")
        sleep(200)
