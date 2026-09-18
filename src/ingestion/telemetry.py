import math
import random
from datetime import datetime

def generate_telemetry(timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()
    hour = timestamp.hour + timestamp.minute / 60.0 + timestamp.second / 3600.0
    if 6.0 <= hour <= 18.0:
        sun_angle = math.sin(math.pi * (hour - 6.0) / 12.0)
        solar_kw = 80.0 * sun_angle + random.uniform(-2.0, 2.0)
        solar_kw = max(0.0, min(80.0, solar_kw))
    else:
        solar_kw = 0.0
    m_peak = math.exp(-((hour - 8.0) ** 2) / 8.0)
    e_peak = math.exp(-((hour - 20.0) ** 2) / 12.0)
    base_load = 30.0 + 40.0 * m_peak + 60.0 * e_peak
    load_kw = base_load + random.uniform(-4.0, 4.0)
    load_kw = max(10.0, min(150.0, load_kw))
    voltage = 230.0 + random.uniform(-3.0, 3.0)
    current = (load_kw * 1000.0) / voltage if voltage > 0 else 0.0
    frequency = 50.0 + random.uniform(-0.1, 0.1)

    return {
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "solar_kw": round(solar_kw, 2),
        "load_kw": round(load_kw, 2),
        "voltage": round(voltage, 2),
        "current": round(current, 2),
        "frequency": round(frequency, 2)
    }