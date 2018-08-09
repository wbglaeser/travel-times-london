########################################
### IMPORT MODULES                   ###
########################################
import pandas as pd
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyAj5JExaDTeWni5CWXLr8AK4j6Bh8EJDAk')

########################################
### LOOP THROUGH BOROUGHS ###
########################################
london_boroughs = ['Barking and Dagenham',
                   'Barnet',
                   'Bexley',
                   'Brent',
                   'Bromley',
                   'Camden',
                   'City of London',
                   'Croydon',
                   'Ealing',
                   'Enfield',
                   'Greenwich',
                   'Hackney',
                   'Hammersmith and Fulham',
                   'Haringey',
                   'Harrow',
                   'Havering',
                   'Hillingdon',
                   'Hounslow',
                   'Islington',
                   'Kensington and Chelsea',
                   'Kingston upon Thames',
                   'Lambeth',
                   'Lewisham',
                   'Merton',
                   'Newham',
                   'Redbridge',
                   'Richmond upon Thames',
                   'Southwark',
                   'Sutton',
                   'Tower Hamlets',
                   'Waltham Forest',
                   'Wandsworth',
                   'Westminster']
borough_coordinates = dict()
for location in london_boroughs:
    geocode_result = gmaps.geocode(location + 'Borough of London, London, United Kingdom')
    lat = geocode_result[0].get('geometry').get(
            'location'
        ).get(
            'lat'
        )
    lng = geocode_result[0].get('geometry').get(
            'location'
        ).get(
            'lng'
        )
    borough_coordinates[location] = (lat, lng)

df = pd.DataFrame.from_dict(borough_coordinates, orient='index')
df.reset_index(level=0, inplace=True)
df.columns = ['Borough','Latitude','Longitude']

########################################
### STORE DATA ###
########################################
df.to_csv('dataset/borough_coordinates.csv', sep=',', encoding='utf-8', index=False)
