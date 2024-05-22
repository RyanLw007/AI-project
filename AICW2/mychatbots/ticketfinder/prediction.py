import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from lazypredict.Supervised import LazyRegressor
import datetime

# Load the dataset
file_path = '/content/LIVST_NRCH_OD_a51_2020_12_12.csv'
data = pd.read_csv(file_path)

# Drop columns with over 99% missing values and handle other missing data
columns_to_drop = ['dep_wet', 'pass_wet', 'arr_wet', 'arr_et', 'dep_et']
data_cleaned = data.drop(columns=columns_to_drop)
data_cleaned.dropna(subset=['arr_at', 'dep_at'], inplace=True)

# Convert time columns to datetime format
time_columns = ['pta', 'ptd', 'wta', 'wtp', 'wtd', 'arr_at', 'dep_at', 'pass_at']
for col in time_columns:
    data_cleaned[col] = pd.to_datetime('2020-12-12 ' + data_cleaned[col], errors='coerce', format='%Y-%m-%d %H:%M')

# Calculate delays and travel times
data_cleaned['arrival_delay'] = (data_cleaned['arr_at'] - data_cleaned['pta']).dt.total_seconds() / 60
data_cleaned['departure_delay'] = (data_cleaned['dep_at'] - data_cleaned['ptd']).dt.total_seconds() / 60
data_cleaned['travel_time_to_next'] = data_cleaned.groupby('rid')['arr_at'].shift(-1) - data_cleaned['dep_at']
data_cleaned['travel_time_to_next'] = data_cleaned['travel_time_to_next'].dt.total_seconds() / 60

# One-hot encode the 'tpl' variable
tpl_encoded = pd.get_dummies(data_cleaned['tpl'], prefix='station')
data_model_ready = data_cleaned.join(tpl_encoded)

# Remove datetime and non-numeric columns
X = data_model_ready.drop(['rid', 'tpl', 'arr_at', 'dep_at', 'arr_atRemoved', 'dep_atRemoved'], axis=1)
X = X.select_dtypes(include=[np.number])

# Ensure that the target vector y is prepared before filtering X
y = data_model_ready['arrival_delay']
non_na_indices = y.notna()  # Get boolean mask where y is not NaN

# Filter X and y to remove any rows where y is NaN
X_filtered = X[non_na_indices]
y_filtered = y[non_na_indices]

# Handle missing values in features
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X_filtered)  # Impute only after filtering

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y_filtered, test_size=0.2, random_state=42)

# Use LazyPredict to find the best model
lazy_reg = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
models, predictions = lazy_reg.fit(X_train, X_test, y_train, y_test)
best_model = models.index[0]

# Train the best model on the entire dataset
best_model_instance = models[best_model][0]
best_model_instance.fit(X_train, y_train)

# Function to predict future train delays
def future_trains(origin, dest, date, time):
    # Preprocess the input
    dep_time = pd.to_datetime(date + ' ' + time)
    origin_encoded = [0] * len(tpl_encoded.columns)
    dest_encoded = [0] * len(tpl_encoded.columns)
    if 'station_' + origin in tpl_encoded.columns:
        origin_encoded[tpl_encoded.columns.get_loc('station_' + origin)] = 1
    if 'station_' + dest in tpl_encoded.columns:
        dest_encoded[tpl_encoded.columns.get_loc('station_' + dest)] = 1
    
    # Create a single input vector
    input_data = np.array([dep_time.hour] + origin_encoded + dest_encoded).reshape(1, -1)
    
    # Impute missing values if any
    input_data = imputer.transform(input_data)
    
    # Predict using the best model
    prediction = best_model_instance.predict(input_data)
    
    return prediction[0]

# Function to predict delays for active trains
def active_trains(cur_stat, dest, delay):
    # Preprocess the input
    cur_stat_encoded = [0] * len(tpl_encoded.columns)
    dest_encoded = [0] * len(tpl_encoded.columns)
    if 'station_' + cur_stat in tpl_encoded.columns:
        cur_stat_encoded[tpl_encoded.columns.get_loc('station_' + cur_stat)] = 1
    if 'station_' + dest in tpl_encoded.columns:
        dest_encoded[tpl_encoded.columns.get_loc('station_' + dest)] = 1
    
    # Create a single input vector
    input_data = np.array([delay] + cur_stat_encoded + dest_encoded).reshape(1, -1)
    
    # Impute missing values if any
    input_data = imputer.transform(input_data)
    
    # Predict using the best model
    prediction = best_model_instance.predict(input_data)
    
    return prediction[0]

if __name__ == '__main__':
    # Test the functions
    print(active_trains('CLCHSTR', 'NRCH', 5))

