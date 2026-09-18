import os
import sqlite3

DB_PATH = os.path.join("data", "microgrid.db")

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            solar_kw REAL,
            load_kw REAL,
            battery_soc REAL,
            predicted_solar_kw REAL,
            predicted_load_kw REAL,
            battery_cmd_kw REAL,
            grid_cmd_kw REAL,
            shed_cmd_kw REAL,
            system_state TEXT,
            optimization_cost REAL
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()