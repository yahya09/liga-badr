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

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if 'reply_to_message' in msg:#it's a reply
        reply = replyhandler.handle(msg)
        bot.sendMessage(chat_id, reply)
    elif msg['text'].strip() == '/klasemen':
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
        reply += ('Klasemen di atas belum menggunakan tie break.'
                  ' Versi lebih akurat cek: http://challonge.com/badrleague')
        bot.sendMessage(chat_id, reply)
    elif msg['text'].strip() == '/start' or msg['text'].strip() == '/help':
        reply = "BADR(o)BOT v0.2.1\n"
        reply += "Command yg tersedia:\n"
        reply += "/klasemen - melihat klasemen saat ini\n"
        reply += "/updateskor - khusus admin (@yahyaman)\n\n"
        reply += "Coming soon:\n"
        reply += "/jadwal - melihat jadwal player\n"
        reply += "/skor - melihat histori hasil pertandingan player\n"
        reply += "/teamhistory - melihat histori tim yg digunakan player\n"
        bot.sendMessage(chat_id, reply)
    elif msg['text'].strip() == '/updateskor':
        reply = 'Command ini khusus Admin! Situ siapa? :p'
        force = None
        if msg['from']['id'] == ADMIN_ID:
            reply = 'Update skor dgn membalas chat ini:\n'
            reply += 'player1 tim1 skor1 player2 tim2 skor2\n'
            reply += 'Contoh:\n'
            reply += 'yahya juve 2 amri chelsea 1'
            force = ForceReply(force_reply=True, selective=True)

        bot.sendMessage(chat_id, reply, reply_to_message_id=msg['message_id'], reply_markup=force)
    elif msg['text'].strip() == '/teamhistory':
        reply = 'Pilih player:'
        players = herokudb.getPlayerList()
        count = 0
        buttons = []
        btn_row = []
        for player in players:
            count += 1
            data = "history-" + str(player[0])
            btn_row.append(InlineKeyboardButton(text=player[1], callback_data=data))
            if count % 3 == 0:
                buttons.append(btn_row)
                btn_row = []
        #add last btns if present
        if len(btn_row) > 0:
            buttons.append(btn_row)

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        bot.sendMessage(chat_id, reply, reply_markup=keyboard)
    else:
        bot.sendMessage(chat_id, "On progress!")

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    msg_id = telepot.message_identifier(msg['message'])
    bot.editMessageReplyMarkup(msg_id)
    bot.answerCallbackQuery(query_id, text='Sip, oke!')
    reply = "Maaf, ada kesalahan :("
    if 'history' in query_data:
        name = query_data.split('-')[1]
        teams = herokudb.getTeamHistory(name)
        reply = "Team history for %s:\n" % name.upper()
        for key, team in enumerate(teams):
            reply += "{}. {} ({})\n".format(key+1, team[3].lower().title(), team[4])

    #send result to existing message
    bot.editMessageText(msg_id, reply)


bot = telepot.Bot(BOT_KEY)
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')

while 1:
    time.sleep(10)