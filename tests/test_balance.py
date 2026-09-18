from src.core.balance import compute_net_balance, classify_state

def test_compute_net_balance():
    assert compute_net_balance(50.0, 80.0) == 30.0
    assert compute_net_balance(100.0, 40.0) == -60.0
    assert compute_net_balance(50.0, 50.0) == 0.0

def test_classify_state():
    assert classify_state(-10.0, 50.0, 0.0) == "SURPLUS_CHARGING"
    assert classify_state(-10.0, 90.0, 0.0) == "BALANCED"
    assert classify_state(20.0, 50.0, 0.0) == "DEFICIT_DISCHARGING"