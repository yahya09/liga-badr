import herokudb

def handleReply(msg):
    if 'reply_to_message' not in msg:
        return 'Gak tau reply yg mana :('
    
    if 'Update' in msg['reply_to_message']['text']:

