def compute_net_balance(solar_kw, load_kw):
    net_deficit = load_kw - solar_kw
    return net_deficit

def classify_state(net_deficit, battery_soc, grid_draw):
    if net_deficit <= 0:
        return "SURPLUS_CHARGING" if battery_soc < 90.0 else "BALANCED"
    if battery_soc > 20.0:
        return "DEFICIT_DISCHARGING"
    if grid_draw > 100.0:
        return "CRITICAL_THROTTLING"
    return "BALANCED"