import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json
import herokudb

BOT_KEY = '169195335:AAHlZK-qs-gTCaubLevcxZ5jPLRrcX13Ftc'
CHALLONGE_KEY = '3pNNzfwKxLzfqY0azrxIL2xUArraAlBlWgZ7mXyh'
TOURNAMENT_ID = 3133599

users = []

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # buttons = []
    # btns = []
    # count = 0
    # for user in users:
    #     count += 1
    #     btns.append(InlineKeyboardButton(text = user['name'], callback_data = str(user['id'])))
    #     if count % 3 == 0:
    #         buttons.append(btns)
    #         btns = []
    # #add last btns if present
    # if len(btns) > 0:
    #     buttons.append(btns)

    # keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    # bot.sendMessage(chat_id, 'Pilih peserta', reply_markup=keyboard)
    if msg['text'] == '/klasemen':
        msg = 'KLASEMEN LIGA BADR 2017\n'
        msg += '=======================\n'
        players = herokudb.getStandings()
        msg += ''
        count = 1
        for player in players:
            msg += "{}. {}   {}-{}-{}  {}\n".format(count, player[0], player[1], player[2], player[3], player[4])
            count += 1

        msg += '=======================\n'
        msg += 'Klasemen di atas belum menggunakan tie break. Versi lebih akurat cek: http://challonge.com/badrleague'
        bot.sendMessage(chat_id, msg)
    elif msg['text'] == '/start' or msg['text'] == '/help':
        msg = "BADR(o)BOT v0.2\n"
        msg += "Command yg tersedia:\n"
        msg += "/klasemen - melihat klasemen saat ini\n\n"
        msg += "Coming soon:\n"
        msg += "/jadwal - melihat jadwal player\n"
        msg += "/skor - melihat histori hasil pertandingan player\n"
        msg += "/teamhistory - melihat histori tim yg digunakan player\n"
        bot.sendMessage(chat_id, msg)
    else:
        #if ''
        bot.sendMessage(chat_id, "On progress!")

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    # if lastMsgId > 0:
    bot.editMessageReplyMarkup(telepot.message_identifier(msg['message']))
    # else:
    #     print('no last message id')
    bot.answerCallbackQuery(query_id, text='Got it')


bot = telepot.Bot(BOT_KEY)
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')

while 1:
    time.sleep(10)