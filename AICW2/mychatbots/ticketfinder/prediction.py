import pandas as pd
from sklearn.model_selection import train_test_split
from lazypredict.Supervised import LazyRegressor
from sklearn.utils import shuffle
from sklearn.linear_model import Ridge
import numpy as np

# Load your dataset
data = pd.read_csv(r'C:\Users\ryanl\Documents\Artificial Intelligence\AI project\AI-project\AICW2\mychatbots\historictraindata\LIVST_NRCH_OD_a51_2020\LIVST_NRCH_OD_a51_2020_12_12.csv')

# Display the first few rows of the dataset
# print(data.head())

# Filter out rows where actual times are missing
data = data.dropna(subset=['arr_at', 'dep_at'])

# Calculate delay in minutes for arrivals and departures
data['arrival_delay'] = (pd.to_datetime(data['arr_at']) - pd.to_datetime(data['arr_et'])).dt.total_seconds() / 60
data['departure_delay'] = (pd.to_datetime(data['dep_at']) - pd.to_datetime(data['dep_et'])).dt.total_seconds() / 60

# Keep only relevant columns
data = data[['tpl', 'arrival_delay', 'departure_delay']]

# Rename columns for clarity
data.columns = ['station_code', 'arrival_delay', 'departure_delay']

# Handle missing delays (if any)
data['arrival_delay'] = data['arrival_delay'].fillna(0)
data['departure_delay'] = data['departure_delay'].fillna(0)

# print(data.head())


# Define the features and target variable
X = data[['station_code', 'departure_delay']]
y = data['arrival_delay']

# One-hot encode the categorical features
X = pd.get_dummies(X, columns=['station_code'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



# Shuffle the training data
X_train, y_train = shuffle(X_train, y_train, random_state=42)

# Train and evaluate multiple regression models
reg = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
models, predictions = reg.fit(X_train, X_test, y_train, y_test)

# Print the performance of the models
# print(models)



# Train the Ridge Regression model
model = Ridge()
model.fit(X_train, y_train)

# Evaluate the model
# print(f"Training score: {model.score(X_train, y_train)}")
# print(f"Testing score: {model.score(X_test, y_test)}")



def active_trains(cur_stat, dest, delay):
    # Create a DataFrame for the input data
    input_data = pd.DataFrame([[cur_stat, delay]], columns=['station_code', 'departure_delay'])

    # One-hot encode the input data
    input_data = pd.get_dummies(input_data, columns=['station_code'])

    # Align the input data with the training data columns
    input_data = input_data.reindex(columns=X_train.columns, fill_value=0)

    # Make a prediction
    prediction = model.predict(input_data)
    
    # Return the prediction
    return prediction[0]

# Example usage
predicted_delay = active_trains('LIVST', 'BTHNLGR', 10)
print(f"Predicted delay: {predicted_delay} minutes")

