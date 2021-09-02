from Telegram.Client.tele import ClientBot
from Telegram.Admin.tele import AdminBot
import threading
from Analysis import stream

admin = AdminBot()
client = ClientBot()
# client bot
polling_thread = threading.Thread(target=client.bot_polling)
polling_thread.daemon = True
polling_thread.start()

# admin bot
polling_thread2 = threading.Thread(target=admin.bot_polling)
polling_thread2.daemon = True
polling_thread2.start()

if __name__ == '__main__':
    stream.run()
