
standings = []
sql = ""
with open('standing.csv', 'r') as f:
	for line in f:
		entry = line.rstrip().split(',')
		player_id = entry[0]
		#print(entry)
		for index in range(1, len(entry), 2):
			#print(player_id, index)
			sql += "INSERT INTO player_team_history(player_id, match_id, team, match_result)\n"
			sql += "VALUES ({}, NULL, '{}', '{}');\n\n".format(player_id, entry[index], entry[index + 1])

with open('history_data.sql', 'w') as m:
 	m.write(sql)

#print(matches2)