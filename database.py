# database.py
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "app.db"
USERS_TXT = "users.txt"  # optional initial file

class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def execute(self, query, params=()):
        cur = self.conn.cursor()
        cur.execute(query, params)
        self.conn.commit()
        return cur

    def query(self, query, params=()):
        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()

    def init_schema(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        );
        """)
        self.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id TEXT,
            category TEXT,
            severity TEXT,
            status TEXT,
            opened_at TEXT,
            resolved_at TEXT
        );
        """)
        self.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT,
            source TEXT,
            num_rows INTEGER,
            size_mb REAL
        );
        """)
        self.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE,
            requester TEXT,
            assigned_to TEXT,
            status TEXT,
            opened_at TEXT,
            resolved_at TEXT,
            priority TEXT
        );
        """)

    def load_sample_data(self):
        data_dir = Path("data")
        it_path = data_dir / "it_tickets.csv"
        if it_path.exists():
            df_it = pd.read_csv(it_path)
            # Avoid duplicate insert on repeated runs: use simple replace for demo
            df_it.to_sql("it_tickets", self.conn, if_exists="append", index=False)

    def migrate_users_from_txt(self):
        if not Path(USERS_TXT).exists():
            return
        with open(USERS_TXT, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    username, password_hash, role = parts[0], parts[1], parts[2]
                    try:
                        self.execute(
                            "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                            (username, password_hash, role),
                        )
                    except Exception:
                        pass

db = DatabaseManager()

if __name__ == "__main__":
    db.init_schema()
    db.migrate_users_from_txt()
    db.load_sample_data()
    print("Database initialized.")
