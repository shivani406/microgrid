def compute_battery_command(net_deficit, current_soc, capacity_kwh, max_charge_kw=50.0, max_discharge_kw=50.0):
    if net_deficit < 0:
        surplus_kw = abs(net_deficit)
        max_possible_charge = ((90.0 - current_soc) / 100.0) * capacity_kwh
        charge_kw = min(surplus_kw, max_charge_kw, max_possible_charge)
        return -abs(charge_kw)
    elif net_deficit > 0:
        if current_soc <= 20.0:
            return 0.0
        max_possible_discharge = ((current_soc - 20.0) / 100.0) * capacity_kwh
        discharge_kw = min(net_deficit, max_discharge_kw, max_possible_discharge)
        return abs(discharge_kw)
    return 0.0