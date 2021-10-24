import time
import pandas as pd
import requests
import json

# This is going to go out to the US Census API to get key information for the address, like lat and long coordinates
# so that we can do some mapping in a later stage of our project

df = pd.read_csv('C:\\Users\\Rober\\Documents\\GitHub\\MSIS5193_BGJRGroup_Project\\Clean Data\\combined.csv')

api_url = 'https://geocoding.geo.census.gov/geocoder/locations/address'

rec_cnt = len(df.index)

cnt = 0

while cnt < rec_cnt:
    street = df.iloc[cnt,0]
    city = df.iloc[cnt,1]
    state = df.iloc[cnt,2]

    # We need to build up the API request with the query string parameters
    full_url = api_url + '?street=' + street.replace(' ','+') + '&city=' + city.strip().replace(' ','+') + '&state=' + state + '&benchmark=2020&format=json'
    response = requests.get(full_url)
    
    # Due to some errors during testing, I've encapsulated this in a try/catch block
    # If we get an error, we're just going to move on to the next record.
    try:
        data = response.json()
    except:
        cnt += 1
        continue

    # The json that results from this API is VERY deep structurally, so we need to move down the tree several
    # levels to get to the elements we need
    
    result = response.json()['result']
    matches = result['addressMatches']

    # If there is no addressMatches element, then the API didn't find data for the provided address.

    if len(matches) < 1:
        cnt += 1
        continue

    matched_address = matches[0]
    coordinates = matched_address['coordinates']
    matched_address_parts = matched_address['addressComponents']

    df.iloc[cnt,14] = coordinates['y'] #Latitude coordinate
    df.iloc[cnt,15] = coordinates['x'] #Longitude coordinate
    df.iloc[cnt,3] = matched_address_parts['zip'] #This gets us a more accurate zipcode
    cnt += 1

df.to_csv('C:\\Users\\Rober\\Documents\\GitHub\\MSIS5193_BGJRGroup_Project\\Final Data\\final_dataset.csv', index=False)