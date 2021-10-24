#import numpy as np
import time
import pandas as pd
import requests
import json

df = pd.read_csv('C:\\Users\\Rober\\Documents\\GitHub\\MSIS5193_BGJRGroup_Project\\Clean Data\\combined.csv')

api_url = 'https://geocoding.geo.census.gov/geocoder/locations/address'

rec_cnt = len(df.index)

cnt = 0

while cnt < rec_cnt:
    street = df.iloc[cnt,0]
    city = df.iloc[cnt,1]
    state = df.iloc[cnt,2]
    full_url = api_url + '?street=' + street.replace(' ','+') + '&city=' + city.strip().replace(' ','+') + '&state=' + state + '&benchmark=2020&format=json'
    response = requests.get(full_url)
    
    try:
        data = response.json()
    except:
        cnt += 1
        continue

    result = response.json()['result']
    matches = result['addressMatches']

    if len(matches) < 1:
        cnt += 1
        continue

    matched_address = matches[0]
    coordinates = matched_address['coordinates']
    matched_address_parts = matched_address['addressComponents']
    df.iloc[cnt,14] = coordinates['y']
    df.iloc[cnt,15] = coordinates['x']
    df.iloc[cnt,3] = matched_address_parts['zip']
    cnt += 1

df.to_csv('C:\\Users\\Rober\\Documents\\GitHub\\MSIS5193_BGJRGroup_Project\\Final Data\\final_dataset.csv', index=False)