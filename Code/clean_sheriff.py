import numpy as np
import time
import pandas as pd

df = pd.read_csv('c:\\temp\\sheriffsales.csv')

#df = df[['SalesDate','Address','AppraisalValue','beds','baths','sqft','yearbuilt','renoyear']]

df['City'] = np.nan
df['State'] = np.nan
df['Zip'] = np.nan
df['DaysOnMarket'] = np.nan
df['LastSaleDate'] = np.nan
df['SaleType'] = np.nan
df['Lat'] = np.nan
df['Long'] = np.nan


df = df[['Address','City','State','Zip','AppraisalValue','sqft','beds','baths','yearbuilt','renoyear','DaysOnMarket','LastSaleDate','SalesDate','SaleType','Lat','Long']]

record_count = len(df.index)

cnt = 0

while cnt < record_count:
    address = df.iloc[cnt,0]
    address_parts = address.replace('(RECALLED)','').split(',')
    street = address_parts[0].strip()
    city = address_parts[1].strip()
    state = 'OK'
    df.iloc[cnt,0] = street
    df.iloc[cnt,1] = city
    df.iloc[cnt,2] = state
    df.iloc[cnt,13] = 'Sheriff'
    cnt += 1

df.to_csv('C:\\Users\\Rober\\Documents\\GitHub\\MSIS5193_BGJRGroup_Project\\Clean Data\\sheriffsales_clean.csv', index=False)