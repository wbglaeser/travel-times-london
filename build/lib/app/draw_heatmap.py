########################################
### IMPORT MODULES                   ###
########################################
from geopy.distance import great_circle
from collections import defaultdict
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from random import uniform
from scipy.interpolate import griddata

########################################
### LOAD DATA                        ###
########################################
# Prepare Transit Data Tables
df_transit = pd.read_csv('dataset/full_routes.csv')
df_AZIP = df_transit[['Orig_Zip', 'Orig_Lon', 'Orig_Lat']]
df_AZIP.columns = ['Zip', 'Lon', 'Lat']
df_BZIP = df_transit[['Dest_Zip', 'Dest_Lon', 'Dest_Lat']]
df_BZIP.columns = ['Zip', 'Lon', 'Lat']
df_STACK = pd.concat([df_AZIP,df_BZIP])
df_STACK = df_STACK.reset_index()

# Prepare Full London Zips
df_london = pd.read_csv('dataset/london_selection.csv')

########################################
### SET EXAMPLE ZIP                  ###
########################################
# Obtain Coordinates for Start/Destination
zip_ = list(df_london.Postcode)
lat_ = list(df_london.Latitude)
lon_ = list(df_london.Longitude)
zip_to_coos = dict(zip(zip_, zip(lat_, lon_)))
zip_to_coos_ = dict(zip(zip_, zip(lon_,lat_)))

# Select correct coordinates
print('Type in the Postcode (Respect spaces please):')
zip_code = input()
example_coos = zip_to_coos_[zip_code]

########################################
### COMPUTE DISTANCES                ###
########################################
df_stack_dict = dict(zip(list(df_STACK.index),zip(list(df_STACK.Lon),list(df_STACK.Lat))))
distance_dict = {}
for k, dist_coos in df_stack_dict.items():
    distance_dict[k] = great_circle(example_coos, dist_coos).meters
df_dis = pd.DataFrame.from_dict(distance_dict, orient='index')
df_STACK['Distance'] = df_dis[0]

# Select closest points
df_STACK = df_STACK.sort_values('Distance')
df_close = df_STACK[df_STACK.Distance < 1000]
print(len(df_close))
df_close.reset_index(inplace=True)

########################################
### ASSIGN TRANSIT TIMES             ###
########################################
# Prepare data for fast processing
orig_list = list(df_transit['Orig_Zip'])
dest_list = list(df_transit['Dest_Zip'])
trans_list = list(df_transit['Transit'])
orig_to_dest = defaultdict(list)
dest_to_orig = defaultdict(list)
for k, v in zip(orig_list, dest_list):
    orig_to_dest[k].append(v)
for k, v in zip(dest_list, orig_list):
    dest_to_orig[k].append(v)
a_to_b_dict = dict(zip(zip(orig_list, dest_list),trans_list))
b_to_a_dict = dict(zip(zip(dest_list, orig_list),trans_list))
transit_times = defaultdict(dict)
close_dict = df_close['Zip'].to_dict()

# Obtain travel times
for zip_idx in set(close_dict.values()):
    a_to_b = set(orig_to_dest[zip_idx])
    b_to_a = set(dest_to_orig[zip_idx])
    for dzip1 in a_to_b:
        transit_times[zip_idx][dzip1] = a_to_b_dict[(zip_idx, dzip1)]
    for dzip2 in b_to_a:
        transit_times[zip_idx][dzip2] = b_to_a_dict[(zip_idx, dzip2)]

# Convert back to pandas
start_ids = []
frames = []
for start_id, d in transit_times.items():
    start_ids.append(start_id)
    frames.append(pd.DataFrame.from_dict(d, orient='index'))
df_prop = pd.concat(frames, keys=start_ids)
for i in range(2):
    df_prop.reset_index(level=0, inplace=True)
df_prop.columns = ['Destination', 'Origin', 'Transit_Times']

df_prop['Lat'] = df_prop['Destination'].apply(lambda x: zip_to_coos[x][0])
df_prop['Lon'] = df_prop['Destination'].apply(lambda x: zip_to_coos[x][1])
df_prop['Transit_Times'] = df_prop['Transit_Times'].apply(lambda x: x/60)

########################################
### PREPARE DATA FOR MAP             ###
########################################
df = pd.read_csv('dataset/final_data.csv')
x = df.Lon
y = df.Lat
z = df.Transit_Times
ngridx = 50
ngridy = 50

# Load borough coordinates
bos = pd.read_csv('dataset/borough_coordinates.csv')
bos = bos[bos.Latitude <= max(y)]
bos = bos[bos.Latitude >= min(y)]
bos = bos[bos.Longitude <= max(x)]
bos = bos[bos.Longitude >= min(x)]
bgs_lat = list(bos.Latitude)
bgs_lng = list(bos.Longitude)
bgs_txt = list(bos.Borough)

########################################
### PLOT GRAPH                       ###
########################################
plt.figure(figsize=(8,8))
xi = np.linspace(min(x), max(x), ngridx)
yi = np.linspace(min(y), max(y), ngridy)
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='linear')
plt.contour(xi, yi, zi, 14, linewidths=0.5, colors='k')
cntr1 = plt.contourf(xi, yi, zi, 14, cmap="RdBu_r",alpha=0.7)
plt.colorbar(cntr1)
plt.scatter(bgs_lng , bgs_lat, c='green')
for i, txt in enumerate(bgs_txt):
    plt.annotate(txt, (bgs_lng[i],bgs_lat[i]+ 0.007 * uniform(0,1)), size=10)
plt.show()