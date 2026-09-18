import os
import math
import numpy as np
import pandas as pd

def generate_synthetic_solar_data(n_days=365):
    timestamps = pd.date_range(start="2025-01-01 00:00:00", periods=n_days * 24, freq="1h")
    data = []
    for ts in timestamps:
        hour = ts.hour
        month = ts.month
        day_of_year = ts.dayofyear
        if 6 <= hour <= 18:
            sun_angle = math.sin(math.pi * (hour - 6) / 12)
            max_rad = 1000.0 * sun_angle
        else:
            sun_angle = 0.0
            max_rad = 0.0
        cloud_cover = float(np.clip(np.random.normal(30, 20), 0, 100))
        shortwave = max_rad * (1.0 - 0.75 * (cloud_cover / 100.0))
        direct = shortwave * (1.0 - (cloud_cover / 100.0))
        temp = 20.0 + 10.0 * math.sin(math.pi * (hour - 9) / 12) + np.random.normal(0, 2)
        humidity = float(np.clip(70.0 - 0.5 * temp + np.random.normal(0, 5), 20, 95))
        if sun_angle > 0:
            efficiency = 1.0 - 0.005 * max(0.0, temp - 25.0) - 0.001 * max(0.0, humidity - 60.0)
            solar_kw = (shortwave / 1000.0) * 80.0 * efficiency + np.random.normal(0, 1)
            solar_kw = float(np.clip(solar_kw, 0.0, 80.0))
        else:
            solar_kw = 0.0
        data.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "hour_of_day": hour,
            "month": month,
            "day_of_year": day_of_year,
            "cloud_cover_pct": round(cloud_cover, 2),
            "shortwave_radiation_wm2": round(shortwave, 2),
            "direct_radiation_wm2": round(direct, 2),
            "temperature_c": round(temp, 2),
            "humidity_pct": round(humidity, 2),
            "solar_generation_kw": round(solar_kw, 2)
        })
    return pd.DataFrame(data)

def generate_synthetic_load_data(n_days=365):
    timestamps = pd.date_range(start="2025-01-01 00:00:00", periods=n_days * 24, freq="1h")
    data = []
    holidays = {"01-01", "01-26", "05-01", "08-15", "10-02", "12-25"}
    for ts in timestamps:
        hour = ts.hour
        day_of_week = ts.dayofweek
        month = ts.month
        is_weekend = 1 if day_of_week >= 5 else 0
        date_str = ts.strftime("%m-%d")
        is_holiday = 1 if date_str in holidays else 0
        is_peak = 1 if (7 <= hour <= 9 or 18 <= hour <= 21) else 0
        m_peak = math.exp(-((hour - 8) ** 2) / 8.0)
        e_peak = math.exp(-((hour - 20) ** 2) / 12.0)
        base_curve = 30.0 + 40.0 * m_peak + 60.0 * e_peak
        if is_weekend or is_holiday:
            base_curve *= 0.80
        temp = 20.0 + 10.0 * math.sin(math.pi * (hour - 9) / 12) + np.random.normal(0, 2)
        wind_speed = float(np.clip(np.random.normal(3.5, 1.5), 0.5, 12.0))
        hvac_load = max(0.0, temp - 24.0) * 2.5
        load_kw = base_curve + hvac_load + np.random.normal(0, 3)
        load_kw = float(np.clip(load_kw, 10.0, 150.0))
        data.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "hour_of_day": hour,
            "day_of_week": day_of_week,
            "month": month,
            "is_weekend": is_weekend,
            "is_holiday": is_holiday,
            "temperature_c": round(temp, 2),
            "wind_speed_m_s": round(wind_speed, 2),
            "is_peak_hour": is_peak,
            "load_demand_kw": round(load_kw, 2)
        })
    return pd.DataFrame(data)

def prepare_features(df, model_type):
    df_feat = df.copy()
    df_feat["sin_hour"] = np.sin(2 * np.pi * df_feat["hour_of_day"] / 24.0)
    df_feat["cos_hour"] = np.cos(2 * np.pi * df_feat["hour_of_day"] / 24.0)
    if model_type == "solar":
        df_feat["sin_month"] = np.sin(2 * np.pi * df_feat["month"] / 12.0)
        df_feat["cos_month"] = np.cos(2 * np.pi * df_feat["month"] / 12.0)
        feature_cols = [
            "hour_of_day", "month", "day_of_year", "cloud_cover_pct",
            "shortwave_radiation_wm2", "direct_radiation_wm2", "temperature_c",
            "humidity_pct", "sin_hour", "cos_hour", "sin_month", "cos_month"
        ]
        target_col = "solar_generation_kw"
    elif model_type == "load":
        df_feat["sin_dow"] = np.sin(2 * np.pi * df_feat["day_of_week"] / 7.0)
        df_feat["cos_dow"] = np.cos(2 * np.pi * df_feat["day_of_week"] / 7.0)
        df_feat["temp_squared"] = df_feat["temperature_c"] ** 2
        feature_cols = [
            "hour_of_day", "day_of_week", "month", "is_weekend", "is_holiday",
            "temperature_c", "wind_speed_m_s", "is_peak_hour", "sin_hour",
            "cos_hour", "sin_dow", "cos_dow", "temp_squared"
        ]
        target_col = "load_demand_kw"
    else:
        raise ValueError("Unknown model_type")
    x = df_feat[feature_cols]
    y = df_feat[target_col]
    return x, y

def main():
    target_dir = os.path.join("model", "datasets")
    os.makedirs(target_dir, exist_ok=True)
    solar_df = generate_synthetic_solar_data(n_days=365)
    solar_path = os.path.join(target_dir, "solar_training_data.csv")
    solar_df.to_csv(solar_path, index=False)
    load_df = generate_synthetic_load_data(n_days=365)
    load_path = os.path.join(target_dir, "load_training_data.csv")
    load_df.to_csv(load_path, index=False)

if __name__ == "__main__":
    main()