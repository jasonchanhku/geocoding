import pandas as pd
import urllib.request
import json
from tqdm import tqdm

df = pd.read_excel('mapping_parsed_final_test_tableau.xlsx')

#df = df.drop(['AUM'], axis =1)
#print(df.head())
file = open('apikey.txt', 'r')

api = file.read()


lat = []
long = []

print('Geocoding locations..................................')
for row in tqdm(range(0, df.shape[0])):
    response=urllib.request.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address='+df.iloc[row]['Area'].replace(' ', '+')+',+'+df.iloc[row]['District'].replace(' ', '+')+','+df.iloc[row]['Region'].replace(' ', '+')+',+'+'Hong+Kong'+'&key='+api)
    geocode_result = json.load(response)
    x = geocode_result['results'][0]['geometry']['location']['lat']
    y = geocode_result['results'][0]['geometry']['location']['lng']
    lat.append(x)
    long.append(y)

print('All coordinates successfully generated via geocoding')

lat = pd.Series(lat)
long = pd.Series(long)

df['Lat'] = lat.values
df['Long'] = long.values

print('Data Frame Preview')
print(df.head())

df.to_csv('geocoded_data.csv', index=False, encoding = 'utf-8-sig')
print('Data Frame saved with Geocoding data')
