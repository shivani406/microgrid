import os
import sqlite3

def init_database(db_path="data/microgrid.db"):
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS microgrid_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            solar_kw REAL NOT NULL,
            load_kw REAL NOT NULL,
            predicted_solar REAL NOT NULL,
            predicted_load REAL NOT NULL,
            net_deficit REAL NOT NULL,
            battery_soc REAL NOT NULL,
            battery_cmd REAL NOT NULL,
            grid_cmd REAL NOT NULL,
            shed_cmd REAL NOT NULL,
            system_state TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()