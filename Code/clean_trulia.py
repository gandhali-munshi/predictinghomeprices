import numpy as np
import time
import pandas as pd

# The directory where the raw data files are located - specific to my machine
raw_data_dr = 'C:\\Users\\Rober\\Documents\\GitHub\\MSIS5193_BGJRGroup_Project\\Raw Data\\'

# A list of the Trulia files we need to process
files = ['trulia_v1.csv',
    'trulia_v1_otherlisting.csv']

for file in files:

    # Load the file
    df = pd.read_csv(raw_data_dr + file)

    # We need to rename some columns into the common column naming we have so that the combination of the data sets is easier
    df = df.rename(columns={'Price':'AppraisalValue','Bed':'beds','Bath':'baths','LotSize/SqFt':'sqft','Ownership':'SaleType', 'Year build': 'yearbuilt'})

    # Adding in columns we will be using later
    df['City'] = np.nan
    df['State'] = np.nan
    df['Zip'] = np.nan
    df['DaysOnMarket'] = np.nan
    df['LastSaleDate'] = np.nan
    df['Lat'] = np.nan
    df['Long'] = np.nan
    df['renoyear'] = np.nan
    df['SalesDate'] = np.nan

    # Getting the columns in the correct order - again to make combining easier
    df = df[['Address','City','State','Zip','AppraisalValue','sqft','beds','baths','yearbuilt','renoyear','DaysOnMarket','LastSaleDate','SalesDate','SaleType','Lat','Long']]

    record_count = len(df.index)

    cnt = 0

    # Similar to the sheriff's data, we need to break up the address field into its various parts.

    while cnt < record_count:
        address = df.iloc[cnt,0]
        address_parts = address.split(',')
        street = address_parts[0].strip()
        city = address_parts[1].strip()
        state = 'OK'
        df.iloc[cnt,0] = street
        df.iloc[cnt,1] = city
        df.iloc[cnt,2] = state

        # The bed and bath data in these files has a suffix we want to remove so that we are just dealing with numerics
        df.iloc[cnt,6] = str(df.iloc[cnt,6]).replace('bd','')
        df.iloc[cnt,7] = str(df.iloc[cnt,7]).replace('ba','')
        cnt += 1

    df.to_csv('C:\\Users\\Rober\\Documents\\GitHub\\MSIS5193_BGJRGroup_Project\\Clean Data\\' + file.replace('.csv','_clean.csv'), index=False)