import requests
import pandas as pd
import numpy as np
import os

# Create folders
os.makedirs('data', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# Cities
CITIES = {
    'Chennai':   {'lat': 13.08, 'lon': 80.27},
    'Delhi':     {'lat': 28.61, 'lon': 77.21},
    'Bengaluru': {'lat': 12.97, 'lon': 77.59},
}

# Solar panel constants
PANEL_AREA       = 1.6
PANEL_EFFICIENCY = 0.20
TEMP_COEFFICIENT = 0.004
NOCT             = 45


# ✅ FETCH HISTORICAL DATA (FIXED)
def fetch_city_data(city_name, lat, lon):
    print(f'Fetching data for {city_name}...')

    url = 'https://archive-api.open-meteo.com/v1/archive'

    all_data = []

    # Loop through months
    for month in range(1, 13):
        start_date = f'2023-{month:02d}-01'
        end_date   = f'2023-{month:02d}-28'   # safe for all months

        print(f"  -> Month {month}")

        params = {
            'latitude': lat,
            'longitude': lon,
            'start_date': start_date,
            'end_date': end_date,
            'hourly': 'shortwave_radiation,temperature_2m,cloudcover,windspeed_10m,relativehumidity_2m',
            'timezone': 'Asia/Kolkata',
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("Error:", response.text)
            continue

        data = response.json().get('hourly', {})
        df = pd.DataFrame(data)

        if not df.empty:
            all_data.append(df)

    if not all_data:
        print("No data received!")
        return None

    df_all = pd.concat(all_data, ignore_index=True)

    df_all['time'] = pd.to_datetime(df_all['time'])
    df_all['city'] = city_name

    return df_all
# ✅ FEATURE ENGINEERING (CLEANED & IMPROVED)
def engineer_features(df):

    df = df.rename(columns={
        'shortwave_radiation': 'irradiance_ghi',
        'temperature_2m': 'ambient_temp',
        'cloudcover': 'cloud_cover_pct',
        'windspeed_10m': 'wind_speed',
        'relativehumidity_2m': 'humidity_pct',
    })

    # Better missing value handling
    #df = df.fillna(method='ffill').fillna(0)
    df = df.ffill().fillna(0)

    # Cell temperature
    df['cell_temp'] = df['ambient_temp'] + ((NOCT - 20) / 800 * df['irradiance_ghi'])

    # DC Power
    df['dc_power_w'] = (
        PANEL_AREA
        * PANEL_EFFICIENCY
        * df['irradiance_ghi']
        * (1 - TEMP_COEFFICIENT * (df['cell_temp'] - 25))
    ).clip(lower=0)

    # AC Power
    df['ac_power_w'] = df['dc_power_w'] * 0.96
    df['ac_power_kw'] = df['ac_power_w'] / 1000

    # Time features
    df['hour'] = df['time'].dt.hour
    df['month'] = df['time'].dt.month
    df['day_of_year'] = df['time'].dt.dayofyear

    # Day/Night indicator
    df['is_day'] = (df['irradiance_ghi'] > 0).astype(int)

    return df


# ✅ MAIN FUNCTION
def main():
    print("Fetching data...")

    frames = []

    for city, coords in CITIES.items():
        df = fetch_city_data(city, coords['lat'], coords['lon'])

        if df is not None:
            frames.append(df)

    if not frames:
        print("No data collected!")
        return

    df_all = pd.concat(frames, ignore_index=True)

    df_clean = engineer_features(df_all)

    # Save dataset
    df_clean.to_csv('data/solar_data_clean.csv', index=False)

    print("✅ Data saved successfully!")
    print("Shape:", df_clean.shape)
    print("Columns:", df_clean.columns.tolist())


if __name__ == "__main__":
    main()