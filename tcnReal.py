import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras import backend as K
from tcn import TCN

# Load the CSV file
data = pd.read_csv('sorted.csv')

# Convert 'Time' column to datetime format
data['Time'] = pd.to_datetime(data['Time'], format='%Y-%m-%d %H:%M:%S')

# Set 'Time' column as index
data.set_index('Time', inplace=True)

# Resample the data to hourly intervals
data = data.resample('H').mean()

# Remove any rows with missing values
data.dropna(inplace=True)

# Split the data into training and testing sets
train_size = int(len(data) * 0.8)
train_data = data.iloc[:train_size]
test_data = data.iloc[train_size:]

# Standardize the data
scaler = StandardScaler()
train_data_scaled = scaler.fit_transform(train_data)
test_data_scaled = scaler.transform(test_data)

# Define the TCN model
model = Sequential([
    TCN(input_shape=(train_data_scaled.shape[1], 1),
        kernel_size=3, nb_filters=64, dropout_rate=0.2),
    Flatten(),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(loss='binary_crossentropy', optimizer=Adam(
    learning_rate=0.001), metrics=['accuracy'])

# Train the model
early_stopping = EarlyStopping(monitor='val_loss', patience=5)
model.fit(train_data_scaled.reshape(train_data_scaled.shape[0], train_data_scaled.shape[1], 1),
          train_data['Occupancy'].values, epochs=10, batch_size=32,
          validation_split=0.2, callbacks=[early_stopping])

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(test_data_scaled.reshape(test_data_scaled.shape[0], test_data_scaled.shape[1], 1),
                                     test_data['Occupancy'].values)

# Use the model to predict occupancy statistics
predictions = model.predict(test_data_scaled.reshape(
    test_data_scaled.shape[0], test_data_scaled.shape[1], 1))
