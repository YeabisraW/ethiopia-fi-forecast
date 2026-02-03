import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# 1. Initialize data as None
data = None

# Load your unified data
try:
    df = pd.read_csv('data/processed/unified_inclusion_data.csv')
    # Change from 'USG_DIGITAL_PAYMENT' to 'ACC_OWNERSHIP'
    data = df[df['indicator_code'] == 'ACC_OWNERSHIP']['value_numeric'].values.reshape(-1, 1)
    print("✅ Data loaded successfully.")
except FileNotFoundError:
    print("❌ Error: 'unified_inclusion_data.csv' not found. Check the path.")
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")

# 2. Only proceed if data was successfully created
if data is not None:
    # Scaling (Normalization)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # 3. Create Windows (Lookback)
    def create_sequences(dataset, lookback=3):
        X, y = [], []
        for i in range(len(dataset) - lookback):
            X.append(dataset[i:(i + lookback), 0])
            y.append(dataset[i + lookback, 0])
        return np.array(X), np.array(y)

    X, y = create_sequences(scaled_data, lookback=3)
    # Reshape for LSTM: [samples, time steps, features]
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    print(f"✅ Data prepared. X shape: {X.shape}, y shape: {y.shape}")
else:
    print("🛑 Script stopped because no data was loaded.")
# --- Add this to the bottom of notebooks/forecasting_engine.py ---

# 4. Build the LSTM Model
print("🧠 Building the Neural Network...")
model = Sequential([
    LSTM(50, activation='relu', input_shape=(3, 1), return_sequences=False),
    Dropout(0.2),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')

# 5. Train the Model
print("🚀 Training the Forecasting Brain (50 epochs)...")
# We use epochs=50 to find the best fit without overthinking the small dataset
model.fit(X, y, epochs=50, verbose=0) 
print("✅ Training complete!")

# 6. Generate the Multi-Year Forecast (2025-2027)
forecast = []
current_window = scaled_data[-3:].reshape(1, 3, 1)

for _ in range(3):  # Predict 3 steps ahead (2025, 2026, 2027)
    pred_scaled = model.predict(current_window, verbose=0)
    forecast.append(pred_scaled[0, 0])
    
    # Slide the window: remove the first year, add the new prediction
    new_window = np.append(current_window[0, 1:, 0], pred_scaled)
    current_window = new_window.reshape(1, 3, 1)

# 7. Reverse the scaling to get real percentages
forecast_rescaled = scaler.inverse_transform(np.array(forecast).reshape(-1, 1))

print("\n--- 📈 ETHIOPIA FINANCIAL INCLUSION FORECAST ---")
years = [2025, 2026, 2027]
for year, value in zip(years, forecast_rescaled):
    print(f"Year {year}: {value[0]:.2f}%")

# Save results for the final report
forecast_df = pd.DataFrame({'Year': years, 'Forecasted_Inclusion': forecast_rescaled.flatten()})
forecast_df.to_csv('data/processed/long_term_forecast.csv', index=False)
print("\n✅ Forecast saved to data/processed/long_term_forecast.csv")    