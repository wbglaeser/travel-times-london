# -------------------------------------
# Import Modules
#-------------------------------------
import pandas as pd
from math import sqrt
# import matplotlib.pyplot as plt
import csv
from random import sample
import numpy as np
import googlemaps  # imports google maps library
from datetime import datetime
from geopy import distance

gmaps = googlemaps.Client(key='####################################')
sdate = f"{datetime.now():%m_%d_%H_%M}"
cols = [
    'Orig_Zip', 'Dest_Zip', 'Orig_Lon', 'Orig_Lat', 'Dest_Lon', 'Dest_Lat', 'Transit'
]
with open('dataset/routes_{}.csv'.format(sdate), 'w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(cols)
# -------------------------------------
# LOAD CSV
#-------------------------------------
data = pd.read_csv('dataset/London postcodes.csv')
data = data[data['In Use?'] == 'Yes']
keep = ['Postcode', 'Latitude', 'Longitude', 'Population']
df = data[keep]
df['Distance'] = np.zeros(len(df))
df = df[df.Population > 100]
df = df.reset_index()
# Compute distance from centre
for i in range(len(df)):
    df.loc[i, 'Distance'] = distance.distance((-0.115425, 51.512376),(df.loc[i, 'Longitude'],df.loc[i, 'Latitude'])).meters
    print(i / len(df))
cut = df[df['Distance'] < 10000]
cut = cut.reset_index()

fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
axes[0].scatter(df.Longitude, df.Latitude)
axes[1].scatter(cut.Longitude, cut.Latitude)

def draw_connection(df):
    orig_draw = sample(list(df.index), 1)[0]
    dest_draw = sample(list(df.index), 1)[0]
    return orig_draw, dest_draw

full_df = pd.DataFrame(index=range(29000), columns=cols)
for idx in range(25000):
    time_of_travel = datetime(2018, 8, 1, 9, 0)
    orig_draw, dest_draw = draw_connection(cut)
    full_df.loc[idx, 'Orig_Zip'] = cut.loc[orig_draw, 'Postcode']
    full_df.loc[idx, 'Dest_Zip'] = cut.loc[dest_draw, 'Postcode']
    full_df.loc[idx, 'Orig_Lon'] = cut.loc[orig_draw, 'Longitude']
    full_df.loc[idx, 'Orig_Lat'] = cut.loc[dest_draw, 'Latitude']
    full_df.loc[idx, 'Dest_Lon'] = cut.loc[orig_draw, 'Longitude']
    full_df.loc[idx, 'Dest_Lat'] = cut.loc[dest_draw, 'Latitude']
    try:
        transit_directions = gmaps.directions(
            (cut.loc[orig_draw, 'Latitude'], cut.loc[orig_draw, 'Longitude']),
            (cut.loc[dest_draw, 'Latitude'], cut.loc[dest_draw, 'Longitude']),
            mode='transit',
            departure_time=time_of_travel,
        )
        travel_time_atob = transit_directions[0].get('legs')[0].get('duration').get(
            'value'
        )
        full_df.loc[idx, 'Transit'] = travel_time_atob
        with open(
            'dataset/routes_{}.csv'.format(sdate), 'a', encoding='utf-8'
        ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(full_df.iloc[idx])
    except BaseException as e:
        print(e)
    print(idx / 32000)
writer = pd.ExcelWriter('dataset/routelist_{}.xlsx'.format(sdate))
full_df.to_excel(writer, 'Sheet1', index=False)
writer.save()
