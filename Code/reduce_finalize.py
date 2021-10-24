import numpy as np
import pandas as pd

final_data_file = 'C:\\Users\\Rober\\Documents\\GitHub\\MSIS5193_BGJRGroup_Project\\Final Data\\final_dataset.csv'

df = pd.read_csv(final_data_file)

# Get columns named correctly
df = df.rename(columns={'AppraisalValue':'Value'})
df = df.rename(columns={'sqft':'Sqft'})
df = df.rename(columns={'beds':'Beds'})
df = df.rename(columns={'baths':'Baths'})
df = df.rename(columns={'yearbuilt':'BuildYear'})
df = df.rename(columns={'renoyear':'DateLastRemodel'})
df = df.rename(columns={'SalesDate':'NextSaleDate'})
df = df.rename(columns={'SaleType':'SourceType'})
df = df.rename(columns={'Lat':'Latitude'})
df = df.rename(columns={'Long':'Longitude'})

reduced = df[(df.Beds!='100')]

reduced.to_csv(final_data_file, index=False)