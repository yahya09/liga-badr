import psycopg2

DB_URI = "postgres://lxacwhbqdwjnxi:jCXAQYvHj7grBzSXLP7zYb3YCS@ec2-54-243-224-151.compute-1.amazonaws.com:5432/d67n060pic8g12"


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