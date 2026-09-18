from src.core.load_shed import compute_load_shed

def test_grid_import_within_limit():
    grid_cmd, shed_cmd = compute_load_shed(remaining_deficit=80.0, max_grid_import=100.0)
    assert grid_cmd == 80.0
    assert shed_cmd == 0.0

def test_grid_import_exceeds_limit():
    grid_cmd, shed_cmd = compute_load_shed(remaining_deficit=130.0, max_grid_import=100.0)
    assert grid_cmd == 100.0
    assert shed_cmd == 30.0