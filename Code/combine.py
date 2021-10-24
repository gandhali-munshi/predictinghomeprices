import numpy as np
import time
import pandas as pd

# This takes all the cleaned data sets that are still individualized and combine them into one master data set

clean_data_dr = 'C:\\Users\\Rober\\Documents\\GitHub\\MSIS5193_BGJRGroup_Project\\Clean Data\\'

files = ['trulia_v1_clean.csv',
    'trulia_v1_otherlisting_clean.csv',
    'sheriffsales_clean.csv']

df_list = []

for file in files:
    df = pd.read_csv(clean_data_dr + file)
    df_list.append(df)

combined_df = pd.concat(df_list, axis=0, ignore_index=True)

combined_df.to_csv('C:\\Users\\Rober\\Documents\\GitHub\\MSIS5193_BGJRGroup_Project\\Clean Data\\combined.csv', index=False)