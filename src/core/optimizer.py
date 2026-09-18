import math

class DispatchOptimizer:
    def __init__(self, grid_cost_per_kwh=0.15, shed_penalty_per_kwh=2.00, bat_degrade_penalty_per_kwh=0.02):
        self.grid_cost = grid_cost_per_kwh
        self.shed_penalty = shed_penalty_per_kwh
        self.bat_penalty = bat_degrade_penalty_per_kwh

    def evaluate_cost(self, grid_kw, shed_kw, bat_kw):
        cost = (grid_kw * self.grid_cost) + (shed_kw * self.shed_penalty) + (abs(bat_kw) * self.bat_penalty)
        return cost

    def optimize_dispatch(self, predicted_solar_kw, predicted_load_kw, current_soc, capacity_kwh, max_charge_kw=50.0, max_discharge_kw=50.0, max_grid_import=100.0):
        net_deficit = predicted_load_kw - predicted_solar_kw
        if net_deficit <= 0:
            surplus_kw = abs(net_deficit)
            max_possible_charge = ((90.0 - current_soc) / 100.0) * capacity_kwh
            charge_kw = min(surplus_kw, max_charge_kw, max_possible_charge)
            return {
                "battery_cmd_kw": -abs(charge_kw),
                "grid_cmd_kw": 0.0,
                "shed_cmd_kw": 0.0,
                "cost": 0.0
            }
        max_possible_discharge = max(0.0, ((current_soc - 20.0) / 100.0) * capacity_kwh)
        effective_max_discharge = min(net_deficit, max_discharge_kw, max_possible_discharge)
        best_bat_kw = 0.0
        best_grid_kw = min(net_deficit, max_grid_import)
        best_shed_kw = max(0.0, net_deficit - best_grid_kw)
        best_cost = self.evaluate_cost(best_grid_kw, best_shed_kw, best_bat_kw)
        step_size = 1.0
        current_bat_kw = 0.0
        improved = True
        while improved:
            improved = False
            candidates = [current_bat_kw - step_size, current_bat_kw + step_size]
            for candidate_bat in candidates:
                if 0.0 <= candidate_bat <= effective_max_discharge:
                    remaining_after_bat = net_deficit - candidate_bat
                    candidate_grid = min(remaining_after_bat, max_grid_import)
                    candidate_shed = max(0.0, remaining_after_bat - candidate_grid)
                    candidate_cost = self.evaluate_cost(candidate_grid, candidate_shed, candidate_bat)
                    if candidate_cost < best_cost:
                        best_cost = candidate_cost
                        best_bat_kw = candidate_bat
                        best_grid_kw = candidate_grid
                        best_shed_kw = candidate_shed
                        current_bat_kw = candidate_bat
                        improved = True
                        break
        return {
            "battery_cmd_kw": round(best_bat_kw, 2),
            "grid_cmd_kw": round(best_grid_kw, 2),
            "shed_cmd_kw": round(best_shed_kw, 2),
            "cost": round(best_cost, 4)
        }