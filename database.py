import psycopg2
import urllib3
import json

BOT_KEY = '169195335:AAHlZK-qs-gTCaubLevcxZ5jPLRrcX13Ftc'
CHALLONGE_KEY = '3pNNzfwKxLzfqY0azrxIL2xUArraAlBlWgZ7mXyh'
TOURNAMENT_ID = 3133599

http = urllib3.PoolManager()
r = http.request('GET', 'http://httpbin.org/robots.txt')
r.status
r.data

DB_URI = "postgres://lxacwhbqdwjnxi:jCXAQYvHj7grBzSXLP7zYb3YCS@ec2-54-243-224-151.compute-1.amazonaws.com:5432/d67n060pic8g12"
# Connect to an existing database
conn = psycopg2.connect(DB_URI)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
...      (100, "abc'def"))

# Query the database and obtain data as Python objects
cur.execute("SELECT * FROM test;")
cur.fetchone()
(1, 100, "abc'def")

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()