import os
import psycopg2

DB_URI = os.environ['BADR_PGSQL']

def getStandings():
    # Connect to an existing database
    conn = psycopg2.connect(DB_URI)
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Query the database and obtain data as Python objects
    cur.execute("SELECT name, win_count, draw_count, lose_count, total_points FROM player_result ORDER BY total_points DESC;")
    players = cur.fetchall()
    # Close communication with the database
    cur.close()
    conn.close()
    return players

"""
Players is tuple of player. example:
({'name' : 'yahya', 'team' : 'juve', 'goals' : 2}, {'name' : 'amri', 'team' : 'chelsea', 'goals' : 1})
"""
def updateScore(players):
    conn = psycopg2.connect(DB_URI)
    cur = conn.cursor()
    query = "SELECT * FROM match_records WHERE (player1_id=%s AND player2_id=%s) OR (player1_id=%s AND player2_id=%s) ;"
    cur.execute(query, [players[0]['name']])
    match = cur.fetchone()
	   
    return "Success!"