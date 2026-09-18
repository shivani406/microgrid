import sqlite3
from db.schema import DB_PATH

def log_telemetry(solar_kw, load_kw, battery_soc, predicted_solar_kw, predicted_load_kw, battery_cmd_kw, grid_cmd_kw, shed_cmd_kw, system_state, optimization_cost):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO telemetry_logs (
            solar_kw, load_kw, battery_soc, predicted_solar_kw, predicted_load_kw,
            battery_cmd_kw, grid_cmd_kw, shed_cmd_kw, system_state, optimization_cost
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        solar_kw, load_kw, battery_soc, predicted_solar_kw, predicted_load_kw,
        battery_cmd_kw, grid_cmd_kw, shed_cmd_kw, system_state, optimization_cost
    ))
    conn.commit()
    conn.close()