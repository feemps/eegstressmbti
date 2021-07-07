
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from IPython.display import clear_output
import sys

path = '1-acquisition/data/flm_stroop_control_2021-07-07-02.54.17.csv'

df = pd.read_csv(path, low_memory=False)

markers = df['Marker'].copy()

# print(df.head())
count_ans = 0
times = []
time_idx_range = []

for idx,marker in enumerate(markers):
    m = marker.split(",")

    if 'start' in marker:
        start_idx = idx
        start_time = df['timestamps'][start_idx]
        
    elif ('T' in marker) or ('F' in marker) or ('O' in marker) or ('S' in marker):
        ans_idx = idx
        ans_time = df['timestamps'][ans_idx]

        if 'Low' in marker :
            markers[start_idx] = 'L' + m[-1]
        elif 'Mild' in marker:
            markers[start_idx] = 'M' + m[-1]
        else:
            markers[start_idx] = 'H' + m[-1]

        count_ans += 1
        times.append(ans_time-start_time)
        time_idx_range.append(ans_idx-start_idx)
        markers[ans_idx] = '0'
    else: 
        markers[idx] = '0'

for idx,marker in enumerate(markers):
    if 'start' in marker:
        markers[idx] = '0'
    else: pass

df.drop('Marker', axis=1, inplace=True)
df['Markers'] = pd.Series(markers, index = df.index)
# print(df.head())
print(df['Markers'].value_counts())

print(len(times))
print(len(time_idx_range))
print(count_ans)

# df_visual.to_pickle("../data/participants/{par}/01_Data_excel-pd/{file}_perception.pkl".format(par=par, file=file))
# df_imagery.to_pickle("../data/participants/{par}/01_Data_excel-pd/{file}_imagery.pkl".format(par=par, file=file))