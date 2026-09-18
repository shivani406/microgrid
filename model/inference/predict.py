import os
import math
import joblib
import pandas as pd

class Predictor:
    def __init__(self):
        artifacts_dir = os.path.join("model", "saved_models")
        solar_path = os.path.join(artifacts_dir, "solar_model.pkl")
        load_path = os.path.join(artifacts_dir, "load_model.pkl")
        self.solar_model = joblib.load(solar_path) if os.path.exists(solar_path) else None
        self.load_model = joblib.load(load_path) if os.path.exists(load_path) else None

    def predict_solar(self, hour, month, day_of_year, cloud_cover, shortwave, direct, temp, humidity):
        if not self.solar_model:
            return 0.0
        sin_hour = math.sin(2 * math.pi * hour / 24.0)
        cos_hour = math.cos(2 * math.pi * hour / 24.0)
        sin_month = math.sin(2 * math.pi * month / 12.0)
        cos_month = math.cos(2 * math.pi * month / 12.0)
        features = pd.DataFrame([{
            "hour_of_day": hour,
            "month": month,
            "day_of_year": day_of_year,
            "cloud_cover_pct": cloud_cover,
            "shortwave_radiation_wm2": shortwave,
            "direct_radiation_wm2": direct,
            "temperature_c": temp,
            "humidity_pct": humidity,
            "sin_hour": sin_hour,
            "cos_hour": cos_hour,
            "sin_month": sin_month,
            "cos_month": cos_month
        }])
        pred = self.solar_model.predict(features)[0]
        return float(max(0.0, pred))

    def predict_load(self, hour, day_of_week, month, is_weekend, is_holiday, temp, wind_speed, is_peak):
        if not self.load_model:
            return 0.0
        sin_hour = math.sin(2 * math.pi * hour / 24.0)
        cos_hour = math.cos(2 * math.pi * hour / 24.0)
        sin_dow = math.sin(2 * math.pi * day_of_week / 7.0)
        cos_dow = math.cos(2 * math.pi * day_of_week / 7.0)
        temp_squared = temp ** 2
        features = pd.DataFrame([{
            "hour_of_day": hour,
            "day_of_week": day_of_week,
            "month": month,
            "is_weekend": is_weekend,
            "is_holiday": is_holiday,
            "temperature_c": temp,
            "wind_speed_m_s": wind_speed,
            "is_peak_hour": is_peak,
            "sin_hour": sin_hour,
            "cos_hour": cos_hour,
            "sin_dow": sin_dow,
            "cos_dow": cos_dow,
            "temp_squared": temp_squared
        }])
        pred = self.load_model.predict(features)[0]
        return float(max(0.0, pred))