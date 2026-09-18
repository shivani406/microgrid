from src.core.battery import compute_battery_command

def test_battery_charging_surplus():
    cmd = compute_battery_command(net_deficit=-30.0, current_soc=50.0, capacity_kwh=200.0)
    assert cmd == -30.0

def test_battery_max_soc_limit():
    cmd = compute_battery_command(net_deficit=-50.0, current_soc=89.5, capacity_kwh=200.0)
    assert cmd == -1.0

def test_battery_discharging_deficit():
    cmd = compute_battery_command(net_deficit=40.0, current_soc=50.0, capacity_kwh=200.0)
    assert cmd == 40.0

def test_battery_min_soc_limit():
    cmd = compute_battery_command(net_deficit=40.0, current_soc=20.0, capacity_kwh=200.0)
    assert cmd == 0.0