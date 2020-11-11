import pandas as pd
from unidecode import unidecode
import math
import random
import numpy as np
import statistics


splits = pd.read_json('data/leaguepedia_cblol.json')
# schools.info()



es = schools[schools['Elementary, Middle, or High School'] == 'ES']
es = es.dropna(subset=['ISAT Value Add Math'])
print('Total elementary schools:', len(es))
# print(es['ISAT Value Add Math'].values.tolist())
# es.describe()

# Remove n rows
# drop_indices = np.random.choice(es.index, int(len(es)/1.5), replace=False)
# es = es.drop(drop_indices)
print('Sample:', len(es))





distances = []
for i in range(len(es)):
#     percentage = round(i/len(es)*100, 2)
    # Loop for second school, avoiding repetitions (eg. school1-school2 and school2-school1)
    for j in range(i+1, len(es)):
        school1 = es.iloc[i]
        school2 = es.iloc[j]
        distances.append(Haversine(school1['Latitude'], school1['Longitude'], school2['Latitude'], school2['Longitude']))
    print('{}/{}'.format(i+1, len(es)), end='\r')
print('\nDone')

filename = 'data/schools.gml'

# TODO review edges
median = np.median(distances)/2
# stdev = statistics.stdev(distances)/2
with open(filename, 'w') as f:
    tmp = 'graph [\n  directed 0\n'

    for i in range(len(es)):
        tmp += '  node [\n    id ' + str(es.iloc[i]['School ID']) + '\n    isatm "' + str(es.iloc[i]['ISAT Value Add Math']) + '"\n  ]\n'

    f.write(tmp)
    for i in range(len(es)):
        for j in range(i+1, len(es)):
            if (Haversine(es.iloc[i]['Latitude'], es.iloc[i]['Longitude'], es.iloc[j]['Latitude'], es.iloc[j]['Longitude']) < median):
                f.write('  edge [\n    source ' + str(es.iloc[i]['School ID']) +'\n    target ' + str(es.iloc[j]['School ID']) +'\n  ]\n')
        print('{}/{}'.format(i+1, len(es)), end='\r')

    f.write(']')
    print('\nDone')
