import sqlite3

class Database:
    """Local SQLite database manager for storing email analysis history."""
    
    def __init__(self, db_path: str = "analysis_history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    sender TEXT,
                    subject TEXT,
                    final_score REAL,
                    classification TEXT
                )
            """)
            conn.commit()

    def insert_record(self, sender: str, subject: str, score: float, classification: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO history (sender, subject, final_score, classification)
                VALUES (?, ?, ?, ?)
            """, (sender, subject, score, classification))
            conn.commit()

    def get_all_records(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, sender, subject, final_score, classification FROM history ORDER BY id DESC")
            return cursor.fetchall()