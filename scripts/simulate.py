import math
import random
import time
from src.core.control_loop import MicrogridController

def run_continuous_simulation(delay_sec=2.0):
    controller = MicrogridController(battery_capacity_kwh=200.0, initial_soc=50.0)
    step_counter = 0
    while True:
        hour = (step_counter // 2) % 24
        time_of_day = hour + ((step_counter % 2) * 0.5)
        if 6 <= time_of_day <= 18:
            solar_base = 160.0 * math.sin(math.pi * (time_of_day - 6) / 12.0)
            solar_actual = max(0.0, solar_base + random.uniform(-20.0, 20.0))
            irradiance = max(0.0, (solar_actual / 80.0) * 1000.0 + random.uniform(-20.0, 20.0))
        else:
            solar_actual = 0.0
            irradiance = 0.0
        if 8 <= time_of_day <= 22:
            load_actual = 60.0 + random.uniform(-10.0, 20.0)
        else:
            load_actual = 35.0 + random.uniform(-5.0, 10.0)
        temp_c = 22.0 + 8.0 * math.sin(math.pi * (time_of_day - 4) / 20.0) + random.uniform(-1.0, 1.0)
        humidity = max(20.0, min(90.0, 50.0 + random.uniform(-10.0, 10.0)))
        wind_speed = max(0.0, 8.0 + random.uniform(-3.0, 3.0))
        controller.execute_step(
            hour=int(hour),
            month=6,
            temp_c=round(temp_c, 2),
            irradiance=round(irradiance, 2),
            humidity=round(humidity, 2),
            wind_speed=round(wind_speed, 2),
            num_occupants=4,
            is_weekend=0,
            solar_actual_kw=round(solar_actual, 2),
            load_actual_kw=round(load_actual, 2)
        )
        step_counter += 1
        time.sleep(delay_sec)

if __name__ == "__main__":
    run_continuous_simulation(delay_sec=2.0)