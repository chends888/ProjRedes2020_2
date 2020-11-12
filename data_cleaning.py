import pandas as pd
from unidecode import unidecode
import math
import random
import numpy as np
import statistics
from collections import defaultdict



splits = pd.read_json('data/leaguepedia_cblol.json')


teams = list(splits.index.values)
players_teams = defaultdict(list)
cols = list(splits)

# Build all players teams along Splits
for col_idx in range(len(list(splits))):
    for row_idx, team in enumerate(teams):
        if type(splits.iloc[row_idx, col_idx]) == list:
            for player in splits.iloc[row_idx, col_idx]:
                players_teams[player.lower()].append(team)
print(len(players_teams))

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



file = 'data/lol_teams.gml'

with open(file, 'w') as f:
    tmp = 'graph [\n  directed 1\n'

    for team in teams:
        tmp += '  node [\n    id "' + team + '"\n    perf "' + "PLACEHOLDER" + '"\n  ]\n'

    f.write(tmp)

    for edge in teams_edges:
        # for j in range(i+1, len(es)):
            f.write('  edge [\n    source "' + edge[0] +'"\n    target "' + edge[1] +'"\n  ]\n')
        # print('{}/{}'.format(i+1, len(es)), end='\r')

    f.write(']')
    print('\nDone')
