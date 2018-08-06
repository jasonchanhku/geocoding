import pandas as pd
import urllib.request
import json
from tqdm import tqdm

streets = [line.rstrip('\n') for line in open('full.txt')]

file = open('apikey.txt', 'r')
api = file.read()

lat = []
long = []
area = []
region = []
country = []
full = []
fail = []
print('Geocoding locations..................................')
for row in tqdm(range(0, len(streets))):
    try:
        response=urllib.request.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address='+streets[row].replace(' ', '+')+',+'+'Hong+Kong'+'&key='+api)
        geocode_result = json.load(response)
        # length is too unpredictable, just get formatted address first
        full.append(geocode_result['results'][0]['formatted_address'])
        lat.append(geocode_result['results'][0]['geometry']['location']['lat'])
        long.append(geocode_result['results'][0]['geometry']['location']['lng'])
    except:
        fail.append(row)
        continue

print('All coordinates successfully generated via geocoding')

print('length of lat: {}, long: {}, full: {}'.format(len(lat), len(long), len(full)))

df = pd.DataFrame()

street = pd.Series(streets)
full = pd.Series(full)
lat = pd.Series(lat)
long = pd.Series(long)

df['Street'] = streets
df['Full'] = full
df['Lat'] = lat
df['Long'] = long

print(df.head())

df.to_csv('geocoded_data_full.csv', index=False, encoding = 'utf-8-sig')

