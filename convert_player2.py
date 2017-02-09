import json


standings = []
sql = ""
with open('standing.csv', 'r') as f:
	for line in f:
		entry = line.rstrip().split(',')
		sql += "UPDATE player_result SET goals_count={}, conceded_count={}\n".format(entry[1], entry[2])
		sql += "WHERE id = {};\n\n".format(entry[0])

with open('players_data.sql', 'w') as m:
 	m.write(sql)

#print(matches2)