import pandas as pd
from collections import defaultdict


# Team's players for the respective splits
splits_players = pd.read_json('data/leaguepedia_cblol.json')

# Team's performance to the respective splits
splits_perf = pd.read_json('data/leaguepedia_cblol_perf.json')



teams = list(splits_players.index.values)
teams_dict = {}
for team_id, team in enumerate(teams):
    teams_dict[team] = team_id
teams_dict = {value:[key] for key, value in teams_dict.items()}

# Build teams performance
teams_perf = defaultdict(list)
for row_idx in teams_dict.keys():
    for col_idx in range(len(list(splits_perf))):
        perf = splits_perf.iloc[row_idx, col_idx]
        if (perf >= 0):
            teams_perf[row_idx].append(splits_perf.iloc[row_idx, col_idx])

for key, value in teams_perf.items():
    teams_perf[key] = [x for x in teams_perf[key] if x != 'nan']
    teams_dict[key].append(sum(teams_perf[key]) / len(teams_perf[key]))

# teams_perf.dropna().unique().tolist()
# print(teams_perf)
# for key, value in teams_perf.items():
#     for x in value:
#         if(x != 'nan'):
            # print(type(x))
print(teams_perf)

# Build all players teams along Splits
players_teams = defaultdict(list)
for col_idx in range(len(list(splits_players))):
    for row_idx in teams_dict.keys():
        if type(splits_players.iloc[row_idx, col_idx]) == list:
            for player in splits_players.iloc[row_idx, col_idx]:
                players_teams[player.lower()].append(row_idx)
print("Players:", len(players_teams))
print("Teams:", len(teams))
# Remove duplicates maintaining order
# https://blog.finxter.com/how-to-remove-duplicates-from-a-python-list-while-preserving-order/
for key, value in players_teams.items():
    players_teams[key] = list(dict.fromkeys(value))

# Build edges between teams
teams_edges = []
for _, player_teams in players_teams.items():
    if len(player_teams) > 1:
        for i in range(len(player_teams) - 1):
            teams_edges.append((player_teams[i], player_teams[i+1]))

# Remove duplicates maintaining order
teams_edges = list(dict.fromkeys(teams_edges))
print("Edges:", len(teams_edges))


file = 'data/lol_teams.gml'

with open(file, 'w') as f:
    tmp = 'graph [\n  directed 1\n\n'

    for team_id, value in teams_dict.items():
        tmp += '  node [\n    id ' + str(team_id) + '\n    label "' + value[0] + '"\n    perf ' + str(value[1]) + '\n  ]\n'

    f.write(tmp)

    for edge in teams_edges:
            f.write('  edge [\n    source ' + str(edge[0]) +'\n    target ' + str(edge[1]) +'\n  ]\n')

    f.write(']')
    print('\nDone')
