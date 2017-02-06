import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json

lastMsgId = 0

users = []

with open('data.json', 'r') as f:
    s = f.read()
    users = json.loads(s);

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    buttons = []
    btns = []
    count = 0
    for user in users:
        count += 1
        btns.append(InlineKeyboardButton(text = user['name'], callback_data = str(user['id'])))
        if count % 3 == 0:
            buttons.append(btns)
            btns = []
    #add last btns if present
    if len(btns) > 0:
        buttons.append(btns)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    msg = bot.sendMessage(chat_id, 'Pilih peserta', reply_markup=keyboard)
    global lastMsgId
    lastMsgId = msg['message_id']

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    # if lastMsgId > 0:
    bot.editMessageReplyMarkup(telepot.message_identifier(msg['message']))
    # else:
    #     print('no last message id')
    bot.answerCallbackQuery(query_id, text='Got it')

#TOKEN = sys.argv[1]  # get token from command-line
TOKEN = '169195335:AAHlZK-qs-gTCaubLevcxZ5jPLRrcX13Ftc'

bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')

while 1:
    time.sleep(10)