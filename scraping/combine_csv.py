########################################
### IMPORT MODULES                   ###
########################################
import pandas as pd
import numpy as np
import os

########################################
### LOAD DATA                        ###
########################################
# London
df_london = pd.read_csv('./dataset/London postcodes.csv')
df_london = df_london[df_london['In Use?'] == 'Yes']
keep = ['Postcode', 'Latitude', 'Longitude', 'Population']
df_london = df_london[keep]
df_london = df_london.reset_index()
df_london_zip = list(df_london.Postcode)
df_london_lat = list(df_london.Latitude)
df_london_lon = list(df_london.Longitude)
zip_lat = dict(zip(df_london_zip,df_london_lat))
zip_lon = dict(zip(df_london_zip,df_london_lon))

# Transit Times
files = [f for f in os.listdir('./dataset') if 'routes_' in f]
data = [pd.read_csv('dataset/' + f) for f in files]
df_full = pd.concat(data)
keep = ['Orig_Zip', 'Dest_Zip','Transit']
df_full = df_full[keep]
for new in ['Orig_Lon', 'Orig_Lat','Dest_Lon','Dest_Lat']:
    df_full[new] = np.zeros(len(df_full))
df_full.reset_index(inplace=True)

########################################
### Fix lat long                     ###
########################################
for idx in range(len(df_full)):
    orig_zip = df_full.loc[idx, 'Orig_Zip']
    dest_zip = df_full.loc[idx, 'Dest_Zip']
    df_full.loc[idx, 'Orig_Lon'] = zip_lon[orig_zip]
    df_full.loc[idx, 'Orig_Lat'] = zip_lat[orig_zip]
    df_full.loc[idx, 'Dest_Lon'] = zip_lon[dest_zip]
    df_full.loc[idx, 'Dest_Lat'] = zip_lat[dest_zip]
    print(idx/len(df_full))

########################################
### Save Data to                     ###
########################################
df_full.to_csv('dataset/full_routes.csv', sep=',', encoding='utf-8', index=False)



