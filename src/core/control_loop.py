import time
from db.logger import log_telemetry
from model.inference.predict import Predictor
from src.core.battery import BatteryModel
from src.core.optimizer import DispatchOptimizer

class MicrogridController:
    def __init__(self, battery_capacity_kwh=200.0, initial_soc=50.0):
        self.predictor = Predictor()
        self.optimizer = DispatchOptimizer()
        self.battery = BatteryModel(capacity_kwh=battery_capacity_kwh, initial_soc=initial_soc)

    def determine_system_state(self, net_load, battery_cmd):
        if net_load <= 0:
            return "SURPLUS_CHARGING" if battery_cmd < 0 else "SURPLUS_IDLE"
        if battery_cmd > 0:
            return "DEFICIT_DISCHARGING"
        return "DEFICIT_GRID_ONLY"

    def execute_step(self, hour, month, temp_c, irradiance, humidity, wind_speed, num_occupants, is_weekend, solar_actual_kw, load_actual_kw, time_step_hours=1.0):
        pred_solar = self.predictor.predict_solar(hour, month, 170, wind_speed, humidity, irradiance, temp_c, temp_c)
        pred_load = self.predictor.predict_load(hour, is_weekend, month, 0, 0, temp_c, wind_speed, 0)
        current_soc = self.battery.get_soc()
        dispatch = self.optimizer.optimize_dispatch(
            predicted_solar_kw=pred_solar,
            predicted_load_kw=pred_load,
            current_soc=current_soc,
            capacity_kwh=self.battery.capacity_kwh
        )
        bat_cmd = dispatch["battery_cmd_kw"]
        if bat_cmd < 0:
            self.battery.charge(abs(bat_cmd), time_step_hours)
        elif bat_cmd > 0:
            self.battery.discharge(bat_cmd, time_step_hours)
        net_actual = load_actual_kw - solar_actual_kw
        state = self.determine_system_state(net_actual, bat_cmd)
        log_telemetry(
            solar_kw=solar_actual_kw,
            load_kw=load_actual_kw,
            battery_soc=self.battery.get_soc(),
            predicted_solar_kw=round(pred_solar, 2),
            predicted_load_kw=round(pred_load, 2),
            battery_cmd_kw=dispatch["battery_cmd_kw"],
            grid_cmd_kw=dispatch["grid_cmd_kw"],
            shed_cmd_kw=dispatch["shed_cmd_kw"],
            system_state=state,
            optimization_cost=dispatch["cost"]
        )
        return {
            "solar_actual_kw": solar_actual_kw,
            "load_actual_kw": load_actual_kw,
            "predicted_solar_kw": round(pred_solar, 2),
            "predicted_load_kw": round(pred_load, 2),
            "battery_soc": self.battery.get_soc(),
            "dispatch": dispatch,
            "system_state": state
        }

    def run_loop(self, steps=5, interval_sec=1.0):
        for step in range(steps):
            result = self.execute_step(
                hour=12, month=6, temp_c=30.0, irradiance=800.0,
                humidity=40.0, wind_speed=10.0, num_occupants=3, is_weekend=0,
                solar_actual_kw=62.61, load_actual_kw=150.41
            )
            print(f"Step {step + 1}/{steps} | State: {result['system_state']} | SoC: {result['battery_soc']:.2f}% | Cost: ${result['dispatch']['cost']}")
            time.sleep(interval_sec)

if __name__ == "__main__":
    controller = MicrogridController()
    controller.run_loop(steps=3, interval_sec=0.5)