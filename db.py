import os
import sqlite3


def get_db_connection(db_path=None):
    if db_path is None:
        db_path = os.environ.get(
            "DATABASE_PATH",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")
        )
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    conn = get_db_connection(db_path)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE NOT NULL,
                filepath TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()
