import pandas as pd
from sklearn.model_selection import train_test_split
from lazypredict.Supervised import LazyRegressor
from sklearn.utils import shuffle
from sklearn.linear_model import Ridge
import os

year = ("2017")

#load dataset
csv_directory = r'C:\Users\ryanl\Documents\Artificial Intelligence\AI project\AI-project\AICW2\mychatbots\historictraindata\LIVST_NRCH_OD_a51_' + year

csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]

dataframes = []

# Loop through the CSV files and read each one into a dataframe
for file in csv_files:
    file_path = os.path.join(csv_directory, file)
    df = pd.read_csv(file_path)
    dataframes.append(df)

# Concatenate all dataframes into a single dataframe
cdf = pd.concat(dataframes, ignore_index=True)

# Filter out rows where actual times are missing
cdf = cdf[cdf['wtp'].isna() | (cdf['wtp'] == '')]

# convert datatype of time columns to datetime
cdf['arr_at'] = pd.to_datetime(cdf['arr_at'], errors='coerce').dt.time
cdf['pta'] = pd.to_datetime(cdf['pta'], errors='coerce').dt.time
cdf['dep_at'] = pd.to_datetime(cdf['dep_at'], errors='coerce').dt.time
cdf['ptd'] = pd.to_datetime(cdf['ptd'], errors='coerce').dt.time

# Calculate delay
def calculate_time_difference(row):
    if pd.notna(row['arr_at']) and pd.notna(row['pta']):
        arr_at_time = pd.to_datetime(row['arr_at'], format='%H:%M:%S')
        pta_time = pd.to_datetime(row['pta'], format='%H:%M:%S')
        # Calculate the difference in seconds
        diff_seconds = (arr_at_time - pta_time).total_seconds()
        # Convert to hours
        return diff_seconds / 3600
    else:
        return None

cdf['delay'] = cdf.apply(calculate_time_difference, axis=1)

data = cdf[['tpl','pta','ptd','arr_at','dep_at', 'delay']]

data.to_csv(f'data{year}.csv',index=False)

print(data.head())

