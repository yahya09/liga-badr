import telepot
import time
from pprint import pprint

bot = telepot.Bot('169195335:AAHlZK-qs-gTCaubLevcxZ5jPLRrcX13Ftc')

last_msg_id = 1790

def handle(msg):
    pprint(msg)

bot.message_loop(handle)

while 1:
    time.sleep(10)