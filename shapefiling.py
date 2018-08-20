# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 17:24:30 2018

@author: a602637
"""
from contextlib import contextmanager
import pandas as pd
from osgeo import ogr
import json
import string
import gc
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely import ops
from shapely.geometry import shape
from tqdm import tqdm
import time

# Context manager decorator 
@contextmanager
def timer(title):
    t0 = time.time()
    yield
    print("{} - done in {:.0f}s".format(title, time.time() - t0))

# Function to create and pass dictionary of all 18 Districts
def create_dict():

    file = ogr.Open("Hong_Kong_18_Districts\Hong_Kong_18_Districts.shp")
    # Get first layer of the shape file 
    myshape = file.GetLayer(0)
    # Dictionary to store names of all 18 districts
    districts = {}
    
    # For loop to extract all features and store in dictionary for later use
    print('There are {} features in the shapefile and will map the following into a dictionary:'.format(myshape.GetFeatureCount()))
    for i in range(0, myshape.GetFeatureCount()):
        feature = myshape.GetFeature(i)
        first = feature.ExportToJson()
        j = json.loads(first)
        del first
        gc.collect()
        # cap wording of district names, WAN CHAI -> Wan Chai
        print('feature {} is: {}'.format(i+1, string.capwords(j['properties']['ENAME'])))
        print('feature {} type is: {}'.format(i+1, j['geometry']['type']))
        print('--'*17)
        districts[string.capwords(j['properties']['ENAME'])] = j['geometry']
        
    return (districts)
    
def map_districts(db, districts, debug):
    
    coor = []
    
    for x, y in tqdm(zip(db.Latitude, db.Longitude), total = len(db.Latitude)):
        for district in list(districts.keys()):
            if shape(districts[district]).contains(Point(y, x)):
                coor.append(district)
                break
        # else outside of for loop indicates only execute if cant map 
        else:
            coor.append('Others')
                
    db['District'] = pd.Series(coor)
      
    if debug:
        print(db[['Formatted_Address', 'District', 'Latitude', 'Longitude']].head(20))
    else:
        db.to_csv(output_file_name, index = False, encoding='utf-8-sig')
    
    return None
    
def main(debug=False):
    num_rows = 1000 if debug else None
    db = pd.read_csv('address_output_all.csv', nrows=num_rows)
    
    with timer('Creating Dictionaries for District Mapping....'):
        districts = create_dict()
    with timer('Mapping Districts to Dataset..........'):
        map_districts(db, districts, debug)
    
if __name__ == "__main__":
    output_file_name = "data_final.csv"
    with timer("Finished running entire script and saved as csv"):
        main()
    
    






