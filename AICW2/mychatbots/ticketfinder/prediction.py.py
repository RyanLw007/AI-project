import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.impute import SimpleImputer

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



# Plot the distribution of arrival and departure delays
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
data_cleaned['arrival_delay'].dropna().hist(bins=50, ax=axes[0], color='skyblue')
axes[0].set_title('Distribution of Arrival Delays (in minutes)')
axes[0].set_xlabel('Minutes')
axes[0].set_ylabel('Frequency')

data_cleaned['departure_delay'].dropna().hist(bins=50, ax=axes[1], color='lightgreen')
axes[1].set_title('Distribution of Departure Delays (in minutes)')
axes[1].set_xlabel('Minutes')
axes[1].set_ylabel('Frequency')
plt.tight_layout()
plt.show()

# Calculate average delays by station
avg_arrival_delays = data_cleaned.groupby('tpl')['arrival_delay'].mean()
avg_departure_delays = data_cleaned.groupby('tpl')['departure_delay'].mean()

# Plot average delays by station
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

avg_arrival_delays.sort_values().plot(kind='bar', ax=axes[0], color='skyblue')
axes[0].set_title('Average Arrival Delays by Station')
axes[0].set_xlabel('Station')
axes[0].set_ylabel('Average Delay (minutes)')
axes[0].tick_params(labelrotation=90)

avg_departure_delays.sort_values().plot(kind='bar', ax=axes[1], color='lightgreen')
axes[1].set_title('Average Departure Delays by Station')
axes[1].set_xlabel('Station')
axes[1].set_ylabel('Average Delay (minutes)')
axes[1].tick_params(labelrotation=90)

plt.tight_layout()
plt.show()


# Ensure data is sorted by route ID and departure time
data_cleaned.sort_values(by=['rid', 'dep_at'], inplace=True)

# Calculate travel time to next station in minutes
data_cleaned['travel_time_to_next'] = data_cleaned.groupby('rid')['arr_at'].shift(-1) - data_cleaned['dep_at']
data_cleaned['travel_time_to_next'] = data_cleaned['travel_time_to_next'].dt.total_seconds() / 60  # Convert to minutes

# Replace any negative values with NaN or a suitable value (e.g., set them to zero or take absolute values)
data_cleaned['travel_time_to_next'] = data_cleaned['travel_time_to_next'].apply(lambda x: np.abs(x) if x < 0 else x)

# Histogram of travel times to the next station
plt.figure(figsize=(10, 5))
data_cleaned['travel_time_to_next'].dropna().hist(bins=50, color='purple')
plt.title('Distribution of Travel Times to Next Station')
plt.xlabel('Travel Time (minutes)')
plt.ylabel('Frequency')
plt.show()



# Extract hour from arrival and departure times
data_cleaned['arr_hour'] = data_cleaned['arr_at'].dt.hour
data_cleaned['dep_hour'] = data_cleaned['dep_at'].dt.hour

# Calculate average delays by hour of the day
avg_arrival_delays_by_hour = data_cleaned.groupby('arr_hour')['arrival_delay'].mean()
avg_departure_delays_by_hour = data_cleaned.groupby('dep_hour')['departure_delay'].mean()

# Plot average delays by hour of the day
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

avg_arrival_delays_by_hour.plot(kind='bar', ax=axes[0], color='skyblue')
axes[0].set_title('Average Arrival Delays by Hour of Day')
axes[0].set_xlabel('Hour of Day')
axes[0].set_ylabel('Average Delay (minutes)')

avg_departure_delays_by_hour.plot(kind='bar', ax=axes[1], color='lightgreen')
axes[1].set_title('Average Departure Delays by Hour of Day')
axes[1].set_xlabel('Hour of Day')
axes[1].set_ylabel('Average Delay (minutes)')

plt.tight_layout()
plt.show()



# Compute the Pearson correlation matrix for relevant numeric features
correlation_matrix = data_cleaned[['arrival_delay', 'departure_delay', 'travel_time_to_next']].corr()

# Display the correlation matrix
correlation_matrix

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

# Train the RandomForest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict on the test set
y_pred = rf_model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)

# Prepare data for plotting
metrics = ['MSE', 'MAE', 'RMSE']
values = [mse, mae, rmse]

# Create a bar chart
plt.figure(figsize=(8, 5))
plt.bar(metrics, values, color=['blue', 'green', 'red'])
plt.xlabel('Error Metrics')
plt.ylabel('Values')
plt.title('Model Evaluation Metrics')
plt.show()

print(f'MSE: {mse}, MAE: {mae}, RMSE: {rmse}')



