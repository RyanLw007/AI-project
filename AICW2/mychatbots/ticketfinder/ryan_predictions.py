import pandas as pd
from sklearn.model_selection import train_test_split
from lazypredict.Supervised import LazyRegressor
from sklearn.utils import shuffle
from sklearn.linear_model import Ridge
import os

#load dataset
csv_directory = r'C:\Users\ryanl\Documents\Artificial Intelligence\AI project\AI-project\AICW2\mychatbots\historictraindata\LIVST_NRCH_OD_a51_2020'

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
cdf = cdf.dropna(subset=['arr_at', 'dep_at'])

# Calculate delay in minutes for arrivals and departures
cdf['arrival_delay'] = (pd.to_datetime(cdf['arr_at']) - pd.to_datetime(cdf['arr_et'])).dt.total_seconds() / 60
cdf['departure_delay'] = (pd.to_datetime(cdf['dep_at']) - pd.to_datetime(cdf['dep_et'])).dt.total_seconds() / 60

# Keep only relevant columns
cdf = cdf[['tpl', 'arrival_delay', 'departure_delay']]

# Rename columns for clarity
cdf.columns = ['station_code', 'arrival_delay', 'departure_delay']

# Handle missing delays (if any)
cdf['arrival_delay'] = cdf['arrival_delay'].fillna(0)
cdf['departure_delay'] = cdf['departure_delay'].fillna(0)

cdf.to_csv('2020data.csv', index=False)

print(cdf.head())

