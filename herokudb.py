import os
import psycopg2

#DB_URI = os.environ['BADR_PGSQL']
DB_URI = 'postgres://postgres:brokoli@localhost:5432/badr_league'
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
    cursor.execute("SELECT id, name FROM player_result ORDER BY id;")
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
    #get match row
    query = "SELECT * FROM match_records WHERE (player1_id=%s AND player2_id=%s) OR (player1_id=%s AND player2_id=%s);"
    cursor.execute(query, (player1[0], player2[0], player2[0], player1[0]))
    match = cursor.fetchone()
    print(match)
    #update team history
    updateTeamHistory(players)
    #update match record
    updated_match = updateRecord([player1, player2], [players[0][2], players[1][2]], match)
    #update standings
    updateStandings([player1, player2], updated_match)

    return "Success!"

"""
players is list of current player row (tuple),
match record is also db row (tuple)
"""
def updateStandings(players, match_record):
    cursor = conn.cursor()
    #who wins? update w-d-l count, and total points
    if match_record[5] == players[0][0]:    #first player win
        players[0][2] += 1
        players[0][7] += 3
        players[1][4] += 1
    elif match_record[5] == players[1][0]:    #second player win
        players[0][4] += 1
        players[1][2] += 1
        players[1][7] += 3
    else:    #if draw
        players[0][3] += 1
        players[1][3] += 1
        #points
        players[0][7] += 1
        players[1][7] += 1

    #update goals, check who is player1
    if match_record[1] == players[0][0]:
        #scored
        players[0][5] += match_record[3]
        players[1][5] += match_record[4]
        #conceded
        players[0][6] += match_record[4]
        players[1][6] += match_record[3]
    else:
        players[0][5] += match_record[4]
        players[1][5] += match_record[3]
        #conceded
        players[0][6] += match_record[3]
        players[1][6] += match_record[4]



    query = ("UPDATE player_result SET "
        "win_count=%s, draw_count=%s, lose_count=%s, "
        "goals_count=%s, conceded_count=%s, total_points=%s "
        "WHERE id=%s;")
    #first player
    # cursor.execute(query, 
    #     (players[0][2], players[0][3], players[0][4], 
    #         players[0][5], players[0][6], players[0][7], players[0][0]))
    # cursor.execute(query, 
    #     (players[1][2], players[1][3], players[1][4], 
    #         players[1][5], players[1][6], players[1][7], players[1][0]))
    # conn.commit()
    print(players)
    return True


"""
player is [player1, player2]
score is [goal1, goal2]
match record is db row (tuple)
"""
def updateRecord(players, score, match_record):
    #check who player1
    if match_record[1] == players[0][0]:    #first player is player1
        match_record[3] = score[0]
    elif match_record[2] == players[1][0]:    #second player is player1
        match_record[4] = score[0]
    else:
        return "Wrong match record"

    #determine winner, null if draw
    winner = 'NULL'
    if score[0] > score[1]:
        match_record[5] = players[0][0];
    elif score[0] < score[1]:
        match_record[5] = players[1][0];

    match_record[6] = 'complete'
    cursor = conn.cursor()
    query = ("UPDATE match_records SET "
        "player1_goals=%s, player2_goals=%s, winner=%s, status='%s'"
        "WHERE id=%s;")
    # cursor.execute(query, (match_record[3], match_record[4], match_record[5], match_record[6], match_record[0]))
    # conn.commit()
    print(match_record)
    return match_record

def updateTeamHistory(players):
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
    query = "INSERT INTO player_team_history(player_id, match_id, team, match_result) VALUES (%s, %s, '%s', '%s');"
    # cursor.execute(query, (player1_id, match_id, players[0][1].lower(), player1_result))
    # cursor.execute(query, (player2_id, match_id, players[1][1].lower(), player2_result))
    # conn.commit()
    print([player1_result, player2_result])
    return True