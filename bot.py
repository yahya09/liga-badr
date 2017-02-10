import os
import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
import json
import herokudb
import replyhandler

BOT_KEY = os.environ['BADR_BOT_KEY']
CHALLONGE_KEY = os.environ['BADR_CHALLONGE_KEY']
TOURNAMENT_ID = int(os.environ['BADR_TOURNAMENT_ID'])
ADMIN_ID = int(os.environ['BADR_ADMIN_ID']) #it's me

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
        reply = 'KLASEMEN LIGA BADR 2017\n'
        reply += '=======================\n'
        players = herokudb.getStandings()
        reply += ''
        count = 1
        for player in players:
            reply += "{}. {}   {}-{}-{}  {}\n".format(
                count, player[0], player[1], player[2], player[3], player[4])
            count += 1

        reply += '=======================\n'
        reply += 'Klasemen di atas belum menggunakan tie break. \
            Versi lebih akurat cek: http://challonge.com/badrleague'
        bot.sendMessage(chat_id, msg)
    elif msg['text'] == '/start' or msg['text'] == '/help':
        reply = "BADR(o)BOT v0.2\n"
        reply += "Command yg tersedia:\n"
        reply += "/klasemen - melihat klasemen saat ini\n\n"
        reply += "Coming soon:\n"
        reply += "/jadwal - melihat jadwal player\n"
        reply += "/skor - melihat histori hasil pertandingan player\n"
        reply += "/teamhistory - melihat histori tim yg digunakan player\n"
        bot.sendMessage(chat_id, reply)
    elif msg['text'] == '/updateskor':
        reply = 'Command ini khusus Admin! Situ siapa? :p'
        force = None
        if msg['from']['id'] == ADMIN_ID:
            reply = 'Update skor dgn membalas chat ini:\n'
            reply += 'player1 tim1 skor1 - player2 tim2 skor 2\n'
            reply += 'Contoh:\n'
            reply += 'yahya juve 2 - amri chelsea 1'
            force = ForceReply(force_reply=True, selective=True)

        bot.sendMessage(chat_id, reply, reply_to_message_id=msg['message_id'], reply_markup=force)
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