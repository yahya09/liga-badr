import os
import psycopg2
import challonge

DB_URI = os.environ['BADR_PGSQL']
# Connect to an existing database
conn = psycopg2.connect(DB_URI)


def getStandings():
    # Open a cursor to perform database operations
    cursor = conn.cursor()
    # Query the database and obtain data as Python objects
    cursor.execute("SELECT name, win_count, draw_count, lose_count, total_points FROM player_result ORDER BY total_points DESC;")
    players = cursor.fetchall()
    return players

"""
Players list
"""
def getPlayerList():
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM player_result ORDER BY name;")
    players = cursor.fetchall()
    return players

"""
Players is tuple of player. example:
[('yahya', 'juve', 2), ('amri', 'chelsea', 1)]
"""
def updateScore(players):
    if len(players) != 2:
        return "Jumlah player harus tepat 2!"

    cursor = conn.cursor()
    #get player rows
    cursor.execute("SELECT * FROM player_result WHERE LOWER(name)='{}';".format(players[0][0].lower()))
    player1 = cursor.fetchone()
    cursor.execute("SELECT * FROM player_result WHERE LOWER(name)='{}';".format(players[1][0].lower()))
    player2 = cursor.fetchone()
    if player1 is None or player2 is None:
        return "Ada typo di nama nih! gak ketemu di DB :("
    #get match row
    query = "SELECT * FROM match_records WHERE (player1_id=%s AND player2_id=%s) OR (player1_id=%s AND player2_id=%s);"
    cursor.execute(query, (player1[0], player2[0], player2[0], player1[0]))
    match = cursor.fetchone()
    print("updateScore, match record:", match)
    #update team history
    updateTeamHistory(players,
                      {'match_id':match[0], 'player1_id':player1[0], 'player2_id':player2[0]})
    #update match record
    updated_match = updateRecord([player1, player2], [players[0][2], players[1][2]], match)
    #update standings
    updateStandings([player1, player2], updated_match)
    #update to challonge also
    challonge.updateMatchRecord(updated_match)

    return "Success!"

"""
players is list of current player row (tuple),
match record is also db row (tuple)
"""
def updateStandings(players, match_record):
    cursor = conn.cursor()
    print('standing before:', players)
    #who wins? update w-d-l count, and total points
    #NOTE: in heroku db, it's win-lose-draw sequence
    player1 = {'win': players[0][2], 'draw': players[0][4], 'lose': players[0][3],
               'goals': players[0][5], 'conceded': players[0][6], 'points': players[0][7]}
    player2 = {'win': players[1][2], 'draw': players[1][4], 'lose': players[1][3],
               'goals': players[1][5], 'conceded': players[1][6], 'points': players[1][7]}
    if match_record[5] == players[0][0]:    #first player win
        player1['win'] += 1
        player1['points'] += 3
        player2['lose'] += 1
    elif match_record[5] == players[1][0]:    #second player win
        player2['win'] += 1
        player2['points'] += 3
        player1['lose'] += 1
    else:    #if draw
        player1['draw'] += 1
        player2['draw'] += 1
        #points
        player1['points'] += 1
        player2['points'] += 1

    #update goals, check who is player1
    if match_record[1] == players[0][0]:
        #scored
        player1['goals'] += match_record[3]
        player2['goals'] += match_record[4]
        #conceded
        player1['conceded'] += match_record[4]
        player2['conceded'] += match_record[3]
    else:
        player1['goals'] += match_record[4]
        player2['goals'] += match_record[3]
        #conceded
        player1['conceded'] += match_record[3]
        player2['conceded'] += match_record[4]

    query = ("UPDATE player_result SET "
             "win_count=%s, draw_count=%s, lose_count=%s, "
             "goals_count=%s, conceded_count=%s, total_points=%s "
             "WHERE id=%s;")
    #first player
    cursor.execute(query, (player1['win'], player1['draw'], player1['lose'],
                           player1['goals'], player1['conceded'], player1['points'], players[0][0]))
    cursor.execute(query, (player2['win'], player2['draw'], player2['lose'],
                           player2['goals'], player2['conceded'], player2['points'], players[1][0]))
    conn.commit()
    print('standing after:', [player1, player2])
    return True


"""
player is [player1, player2]
score is [goal1, goal2]
match record is db row (tuple)
"""
def updateRecord(players, score, match_record):
    print(players)
    goal1 = 0
    goal2 = 0
    #check who player1
    if match_record[1] == players[0][0]:    #first player is player1
        goal1 = score[0]
        goal2 = score[1]
    elif match_record[1] == players[1][0]:    #second player is player1
        goal2 = score[0]
        goal1 = score[1]
    else:
        return "Wrong match record"

    #determine winner, null if draw
    winner = 'NULL'
    if score[0] > score[1]:
        winner = players[0][0]
    elif score[0] < score[1]:
        winner = players[1][0]

    state = 'complete'
    cursor = conn.cursor()
    query = ("UPDATE match_records SET "
             "player1_goals=%s, player2_goals=%s, winner=%s, status=%s"
             "WHERE id=%s;")
    cursor.execute(query, (goal1, goal2, winner, state, match_record[0]))
    conn.commit()
    new_record = (match_record[0], match_record[1], match_record[2], goal1, goal2, winner, state)
    print("new record:", new_record)
    return new_record

def updateTeamHistory(players, match_data):
    #match result
    player1_result = "draw"
    player2_result = "draw"
    if players[0][2] > players[1][2]:
        player1_result = "win"
        player2_result = "lose"
    elif players[0][2] < players[1][2]:
        player1_result = "lose"
        player2_result = "win"

    cursor = conn.cursor()
    query = "INSERT INTO player_team_history(player_id, match_id, team, match_result) VALUES (%s, %s, %s, %s);"
    cursor.execute(query, (match_data['player1_id'], match_data['match_id'], players[0][1].lower(), player1_result))
    cursor.execute(query, (match_data['player2_id'], match_data['match_id'], players[1][1].lower(), player2_result))
    conn.commit()
    print([player1_result, player2_result])
    return True

def getTeamHistory(name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player_result WHERE LOWER(name)='{}';".format(name))
    player = cursor.fetchone()
    if player is None:
        return "Nama player tidak dikenal!"

    cursor.execute("SELECT * FROM player_team_history WHERE player_id=%s;", (player[0],))
    teams = cursor.fetchall()
    return teams
