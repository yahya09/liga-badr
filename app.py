import telepot
import time
from pprint import pprint
import json

bot = telepot.Bot('169195335:AAHlZK-qs-gTCaubLevcxZ5jPLRrcX13Ftc')

last_msg_id = 1790

users = []

with open('data.json', 'r') as f:
    s = f.read()
    users = json.loads(s);

pprint(users)
#def handle(msg):
#    pprint(msg)

#bot.message_loop(handle)

#while 1:
#    time.sleep(10)