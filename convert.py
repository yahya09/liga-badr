import json

matches = []

with open('match_data.json', 'r') as f:
	content = f.read()
	matches = json.loads(content)

#print(len(matches))

sql = ""
for obj in matches:
	sql += "INSERT INTO match_records(id, player1_id, player2_id, player1_goals, player2_goals, winner, status)\n"
	score = "0-0"
	winner = "NULL"
	#print(obj['match']['state'] == "complete")
	if obj['match']['state'] == 'complete':
		score = obj['match']['scores_csv']
		winner = "NULL" if obj['match']['winner_id'] is None else str(obj['match']['winner_id'])

	sql += "VALUES ({},{},{},{},{},{},'{}');\n\n".format(
		obj['match']['id'], obj['match']['player1_id'], obj['match']['player2_id'], 
		score[0], score[2], winner, obj['match']['state'])

with open('matchdb.sql', 'w') as m:
 	m.write(sql)

#print(matches2)