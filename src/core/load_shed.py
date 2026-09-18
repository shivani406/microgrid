def compute_load_shed(remaining_deficit, max_grid_import=100.0):
    if remaining_deficit <= 0:
        return 0.0, 0.0
    if remaining_deficit <= max_grid_import:
        return remaining_deficit, 0.0
    grid_cmd_kw = max_grid_import
    shed_cmd_kw = remaining_deficit - max_grid_import
    return grid_cmd_kw, shed_cmd_kw