import herokudb
import re

def handle(msg):
    if 'reply_to_message' not in msg:
        return 'Aku gak tau kamu reply yg mana :('

    if 'Update' in msg['reply_to_message']['text']:
        return handleUpdateScore(msg)

    return "On progress!"

def handleUpdateScore(msg):
    print("Handle update score: ", msg['text'])
    pattern = re.compile('^([a-zA-Z]+ ){2}[0-9]+ ([a-zA-Z]+ ){2}[0-9]+$')
    if pattern.match(msg['text'].strip()) is None:
        return "Format salah!"

    queries = msg['text'].split(' ')
    player1 = (queries[0], queries[1], int(queries[2]))
    player2 = (queries[3], queries[4], int(queries[5]))
    result = herokudb.updateScore([player1, player2])
    return result
