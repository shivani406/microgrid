import time
import random
from src.core.control_loop import MicrogridController

def run_simulation(steps=20, delay_sec=2.0):
    controller = MicrogridController(battery_capacity_kwh=200.0, initial_soc=50.0)
    
    for step in range(steps):
        hour = (8 + step) % 24
        temp_c = 25.0 + random.uniform(-2.0, 5.0)
        irradiance = max(0.0, 800.0 - (abs(12 - hour) * 100.0) + random.uniform(-50.0, 50.0))
        humidity = random.uniform(30.0, 60.0)
        wind_speed = random.uniform(5.0, 15.0)
        solar_actual = max(0.0, (irradiance / 1000.0) * 80.0 + random.uniform(-5.0, 5.0))
        load_actual = 100.0 + (abs(14 - hour) * 10.0) + random.uniform(-10.0, 20.0)

        result = controller.execute_step(
            hour=hour,
            month=6,
            temp_c=temp_c,
            irradiance=irradiance,
            humidity=humidity,
            wind_speed=wind_speed,
            num_occupants=4,
            is_weekend=0,
            solar_actual_kw=round(solar_actual, 2),
            load_actual_kw=round(load_actual, 2)
        )

        print(f"[Hour {hour:02d}:00] State: {result['system_state']} | Solar: {result['solar_actual_kw']} kW | Load: {result['load_actual_kw']} kW | Battery SoC: {result['battery_soc']}% | Cost: ${result['dispatch']['cost']}")
        time.sleep(delay_sec)

if __name__ == "__main__":
    run_simulation(steps=20, delay_sec=1.5)