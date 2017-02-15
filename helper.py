import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
import json
import herokudb

def buildPlayerListButtons(prefix):
    players = herokudb.getPlayerList()
    count = 0
    buttons = []
    btn_row = []
    for player in players:
        count += 1
        data = prefix + '-' + str(player[0])
        btn_row.append(InlineKeyboardButton(text=player[1], callback_data=data))
        if count % 3 == 0:
            buttons.append(btn_row)
            btn_row = []
        #add last btns if present
    if len(btn_row) > 0:
        buttons.append(btn_row)

    return buttons
