import numpy as np
import time
import pandas as pd

# Load the raw data file
df = pd.read_csv('c:\\temp\\sheriffsales.csv')

# Add in columns that we will need for the combined data set
df['City'] = np.nan
df['State'] = np.nan
df['Zip'] = np.nan
df['DaysOnMarket'] = np.nan
df['LastSaleDate'] = np.nan
df['SaleType'] = np.nan
df['Lat'] = np.nan
df['Long'] = np.nan

# Get columns in the correct order so that the merge of the various data sets is easier and cleaner
df = df[['Address','City','State','Zip','AppraisalValue','sqft','beds','baths','yearbuilt','renoyear','DaysOnMarket','LastSaleDate','SalesDate','SaleType','Lat','Long']]

record_count = len(df.index)

cnt = 0

# We need to get some of the elements cleaned up. In this data set, the address is scraped with the address field having
# both the street address and the city separated by a comma, so we'll split that into two parts.

while cnt < record_count:
    address = df.iloc[cnt,0]
    address_parts = address.replace('(RECALLED)','').split(',')
    street = address_parts[0].strip()
    city = address_parts[1].strip()
    state = 'OK'
    df.iloc[cnt,0] = street
    df.iloc[cnt,1] = city
    df.iloc[cnt,2] = state
    df.iloc[cnt,13] = 'Sheriff' #SourceType, need to get this filled in for this data
    cnt += 1

# Store this off into a clean data file

df.to_csv('C:\\Users\\Rober\\Documents\\GitHub\\MSIS5193_BGJRGroup_Project\\Clean Data\\sheriffsales_clean.csv', index=False)