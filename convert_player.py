import json

players = []
standings = {}

with open('players_data.json', 'r') as f:
	content = f.read()
	players = json.loads(content)

with open('standing.csv', 'r') as f:
	for line in f:
		entry = line.rstrip().split(',')
		standings[entry[1]] = entry

print(len(standings))

sql = ""
for player in players:
	sql += "INSERT INTO player_result(id, name, win_count, draw_count, lose_count, goals_count, conceded_count, total_points)\n"
	player_id = player["id"]
	name = player["name"]
	win = standings[name][4][0]
	draw = standings[name][4][2]
	lose = standings[name][4][4]
	goals = 0
	conceded = 0
	points = int(float(standings[name][5]))

	sql += "VALUES ({},'{}',{},{},{},{},{},{});\n\n".format(
		player_id, name, win, draw, lose, goals, conceded, points)

with open('players_data.sql', 'w') as m:
 	m.write(sql)

#print(matches2)