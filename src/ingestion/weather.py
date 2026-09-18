import requests
import math
from datetime import datetime

def fetch_weather_forecast(lat=18.52, lon=73.86):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,cloud_cover,shortwave_radiation,direct_radiation,wind_speed_10m"
    try:
        response = requests.get(url, timeout=3.0)
        if response.status_code == 200:
            data = response.json().get("current", {})
            return {
                "temperature_c": float(data.get("temperature_2m", 25.0)),
                "humidity_pct": float(data.get("relative_humidity_2m", 50.0)),
                "cloud_cover_pct": float(data.get("cloud_cover", 20.0)),
                "shortwave_radiation_wm2": float(data.get("shortwave_radiation", 400.0)),
                "direct_radiation_wm2": float(data.get("direct_radiation", 300.0)),
                "wind_speed_m_s": float(data.get("wind_speed_10m", 3.0))
            }
    except Exception:
        pass
    hour = datetime.now().hour
    sun_angle = math.sin(math.pi * (hour - 6) / 12) if 6 <= hour <= 18 else 0.0
    return {
        "temperature_c": 28.0,
        "humidity_pct": 55.0,
        "cloud_cover_pct": 25.0,
        "shortwave_radiation_wm2": round(800.0 * sun_angle, 2),
        "direct_radiation_wm2": round(600.0 * sun_angle, 2),
        "wind_speed_m_s": 3.5
    }